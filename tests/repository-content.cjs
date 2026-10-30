const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {webcrypto} = require('node:crypto');

const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
const bundled = JSON.parse(html.match(/<script id="repository-content" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const runtime = html.split('<script>\n')[1].split('\n</script>')[0].replace(
  /  render\(\);\n\}\)\(\);\s*$/,
  '  globalThis.test={getState:()=>state,freshState,validateState,mergeRepositoryContent,renderNote,getError:()=>repositoryContentError};\n})();'
);
assert(runtime.includes('globalThis.test='));

function openNotebook(saved = null, content = bundled) {
  const elements = new Map();
  function element(id) {
    if (!elements.has(id)) elements.set(id, {
      textContent: id === '#embedded-data' ? 'null' : id === '#repository-content' ? JSON.stringify(content) : '',
      innerHTML: '', addEventListener() {}, classList: {add() {}, remove() {}, toggle() {}}
    });
    return elements.get(id);
  }
  const context = {
    document: {documentElement: {dataset: {notebookId: 'test'}}, querySelector: element, addEventListener() {}},
    window: {addEventListener() {}}, location: {hash: '#/problems'},
    localStorage: {getItem: () => saved}, structuredClone, crypto: webcrypto,
    Date, Set, Map, JSON, Error, String, Number, Array, Math, URL, Blob,
    setTimeout() {}, clearTimeout() {}
  };
  vm.createContext(context);
  vm.runInContext(runtime, context);
  return context.test;
}

const initial = openNotebook();
assert.equal(initial.getError(), '');
assert.equal(initial.getState().problems.length, bundled.problems.length);
assert(initial.getState().topics.some(t => t.id === 'recursion'));
const stairs = initial.getState().problems.find(p => p.number === '70');
assert(stairs && stairs.body.includes('self.climbStairs(n-1) + self.climbStairs(n-2)'));
assert(initial.renderNote(stairs.body).headings.some(h => h.text.includes('interview')));

const old = initial.freshState();
old.problems.push({...structuredClone(stairs), id: 'my-other-problem', number: '999999', topics: ['arrays'], body: '내가 이미 적어둔 개인 노트'});
const upgraded = openNotebook(JSON.stringify(old));
assert.equal(upgraded.getState().problems.find(p => p.id === 'my-other-problem').body, '내가 이미 적어둔 개인 노트');
assert(upgraded.getState().problems.some(p => p.id === stairs.id));

const newerBundle = structuredClone(bundled);
newerBundle.problems.find(p => p.number === '70').body += '\nAn updated repository paragraph.';
newerBundle.topics.find(t => t.id === 'recursion').body += '\nAn updated master paragraph.';
const refreshed = openNotebook(JSON.stringify(initial.getState()), newerBundle);
assert(refreshed.getState().problems.find(p => p.number === '70').body.endsWith('An updated repository paragraph.'));
assert(refreshed.getState().topics.find(t => t.id === 'recursion').body.endsWith('An updated master paragraph.'));

const edited = structuredClone(initial.getState());
edited.problems.find(p => p.number === '70').body += '\nMy browser edit.';
edited.topics.find(t => t.id === 'recursion').body += '\nMy master edit.';
const kept = openNotebook(JSON.stringify(edited), newerBundle);
assert(kept.getState().problems.find(p => p.number === '70').body.endsWith('My browser edit.'));
assert(kept.getState().topics.find(t => t.id === 'recursion').body.endsWith('My master edit.'));

const deleted = structuredClone(initial.getState());
deleted.problems = deleted.problems.filter(p => p.number !== '70');
assert(!openNotebook(JSON.stringify(deleted), newerBundle).getState().problems.some(p => p.number === '70'));

const existingNumber = structuredClone(initial.freshState());
existingNumber.problems.push({...structuredClone(stairs), id: 'my-stairs', topics: ['dp-1d'], body: 'My existing solution.'});
const noDuplicate = openNotebook(JSON.stringify(existingNumber));
assert.equal(noDuplicate.getState().problems.filter(p => p.number === '70').length, 1);
assert.equal(noDuplicate.getState().problems.find(p => p.number === '70').body, 'My existing solution.');

const invalidBundle = structuredClone(bundled);
invalidBundle.problems[0].topics = ['missing-topic'];
const safeFailure = openNotebook(JSON.stringify(edited), invalidBundle);
assert(safeFailure.getError());
assert.equal(safeFailure.getState().problems.find(p => p.number === '70').body, edited.problems.find(p => p.number === '70').body);

const roundtrip = initial.validateState(JSON.parse(JSON.stringify(kept.getState())));
assert.deepEqual(JSON.parse(JSON.stringify(roundtrip)), JSON.parse(JSON.stringify(kept.getState())));
assert.throws(() => initial.validateState({...initial.getState(), repositoryRevisions: {'problem:bad': 'invalid'}}));

console.log('PASS: repository notes appear in existing notebooks; personal edits, deletions, duplicate numbers, validation failures, and JSON roundtrips are preserved.');
