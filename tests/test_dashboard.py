"""Focused stdlib tests for v1.6.0 dashboard/pipeline behavior. Run: python -m unittest discover -s tests"""
import http.client, json, sys, threading, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def get(port, path):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    c.request("GET", path); r = c.getresponse(); body = r.read().decode("utf-8", errors="replace"); c.close()
    return r.status, body

class DashboardApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import dashboard, socketserver
        socketserver.TCPServer.allow_reuse_address = True
        cls.httpd = socketserver.TCPServer(("127.0.0.1", 0), dashboard.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.t = threading.Thread(target=cls.httpd.serve_forever, daemon=True); cls.t.start()
    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown(); cls.httpd.server_close()

    def test_search_pagination_total_and_offset(self):
        s, b = get(self.port, "/api/search?q=lum")
        d = json.loads(b); self.assertEqual(s, 200); self.assertIn("total", d)
        self.assertGreater(d["total"], 50); self.assertEqual(len(d["matches"]), 50)
        s2, b2 = get(self.port, "/api/search?q=lum&offset=50")
        d2 = json.loads(b2); self.assertEqual(d2["offset"], 50)
        self.assertNotEqual(d["matches"][0]["line_num"], d2["matches"][0]["line_num"])

    def test_historical_prompts_source(self):
        s, b = get(self.port, "/api/prompts?source=historical")
        d = json.loads(b); self.assertEqual(s, 200)
        if not d: self.skipTest("historical table not populated yet (run extract_kling_prompts.py)")
        self.assertTrue(all(p.get("source_file") for p in d))
        s2, b2 = get(self.port, "/api/prompts")
        self.assertEqual(len(json.loads(b2)), 102)

    def test_search_hits_carry_session_context(self):
        s, b = get(self.port, "/api/search?q=lum")
        d = json.loads(b); self.assertEqual(s, 200)
        self.assertTrue(all("session" in m for m in d["matches"]))
        self.assertTrue(any(m["session"] for m in d["matches"]), "some hit should name its session")

    def test_doc_allowlist_blocks_traversal(self):
        s, _ = get(self.port, "/api/doc?name=../../dashboard.py")
        self.assertEqual(s, 404)

class ValidatePromptsTests(unittest.TestCase):
    def test_validate_canonical_prompts(self):
        sys.path.insert(0, str(ROOT / "transcribeme"))
        import validate_prompts
        rep = validate_prompts.validate()
        self.assertEqual(rep["canonical"]["total"], 102)
        self.assertIn("with_camera_or_light", rep["canonical"])
        self.assertEqual(rep["historical"]["total"], 177)

class CanonLintTests(unittest.TestCase):
    def test_canon_lint_clean_and_dirty(self):
        sys.path.insert(0, str(ROOT / "transcribeme"))
        import canon_lint
        self.assertEqual(canon_lint.check_text("Bob: I never eat Pop-Tarts.\nLUM: ok", "x.md"), [])
        self.assertTrue(canon_lint.check_text("BOB: I love Pop-Tarts for breakfast.", "x.md"))
        self.assertTrue(canon_lint.check_text("Rob: hello", "x.md"))
        self.assertEqual(canon_lint.check_repo(), [], "repo must pass its own canon gate")

class HistoricalExtractTests(unittest.TestCase):
    def test_parse_all_three_formats(self):
        sys.path.insert(0, str(ROOT / "transcribeme"))
        import extract_kling_prompts as ex
        total = 0
        for fn in ("sitcom_bob_and_lum_DARK_KLING.md", "sitcom_bob_and_lum_episode1_kling.md", "sitcom_bob_and_lum_full_series_kling.md"):
            rows = ex.extract_historical_file(ROOT / fn)
            self.assertGreater(len(rows), 5, fn); total += len(rows)
            self.assertTrue(all(r["prompt_text"] for r in rows), fn)
        self.assertGreater(total, 50)

if __name__ == "__main__":
    unittest.main()
