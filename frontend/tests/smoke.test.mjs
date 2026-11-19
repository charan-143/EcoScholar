import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";

test("login route exists and uses the API auth endpoints",()=>{
  const path="app/login/page.tsx";
  assert.ok(existsSync(path));
  const source=readFileSync(path,"utf8");
  assert.match(source,/\/api\/auth\//);
  assert.match(source,/ecoscholar_token/);
  assert.match(source,/minLength=\{mode==="register"\?10:1\}/);
});
test("frontend API base URL is configurable",()=>{
  const source=readFileSync("app/login/page.tsx","utf8");
  assert.match(source,/NEXT_PUBLIC_API_URL/);
});
