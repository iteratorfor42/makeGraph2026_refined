# -*- coding: utf-8 -*-
"""
test_makegraph.py
------------------
phase2-reproduction/makegraph.py 에 대한 회귀 테스트.

원본 makeGraph2022.exe는 Windows 전용 프로그램이라 이 컨테이너에서
직접 실행/비교할 수 없다. 따라서 여기서는:

  1) 매뉴얼 문서에 기술된 스펙(문법 규칙)을 코드가 정확히 지키는지
  2) 오류 검증 규칙(4대 오류 유형)이 빠짐없이 동작하는지

를 검증한다. Windows 환경이 확보되면 comparison/ 아래에 원본 실행 결과
(.htm)와 재구현 결과(.html)를 나란히 두고 수동/스크립트 비교를 추가한다.

실행:
    cd phase2-reproduction
    python -m unittest tests/test_makegraph.py -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import makegraph as mg  # noqa: E402


class TestParser(unittest.TestCase):
    def test_basic_sections_parse_without_errors(self):
        text = (Path(__file__).resolve().parent.parent / "samples" / "example.lst").read_text(encoding="utf-8")
        result = mg.parse_lst(text)
        self.assertTrue(result.ok, msg=[str(e) for e in result.errors])
        self.assertEqual(len(result.classes), 3)
        self.assertEqual(len(result.relations), 3)
        self.assertEqual(len(result.nodes), 5)
        self.assertEqual(len(result.links), 4)

    def test_unknown_section_name_is_error(self):
        text = "#Klass\nfoo\n"
        result = mg.parse_lst(text)
        self.assertFalse(result.ok)
        self.assertIn("알 수 없는 섹션", result.errors[0].message)

    def test_undefined_class_in_nodes_is_error(self):
        text = "#Class\n사람\n\n#Nodes\n철수 동물 철수\n"
        result = mg.parse_lst(text)
        self.assertFalse(result.ok)
        self.assertTrue(any("Class" in e.message for e in result.errors))

    def test_undefined_relation_in_links_is_error(self):
        text = (
            "#Class\n사람\n\n"
            "#Relation\nlikes\n\n"
            "#Nodes\n철수 사람 철수\n영이 사람 영이\n\n"
            "#Links\n철수 영이 loves\n"
        )
        result = mg.parse_lst(text)
        self.assertFalse(result.ok)
        self.assertTrue(any("Relation" in e.message for e in result.errors))

    def test_undefined_node_in_links_is_error(self):
        text = (
            "#Class\n사람\n\n"
            "#Relation\nlikes\n\n"
            "#Nodes\n철수 사람 철수\n\n"
            "#Links\n철수 민수 likes\n"
        )
        result = mg.parse_lst(text)
        self.assertFalse(result.ok)
        self.assertTrue(any("Node" in e.message for e in result.errors))

    def test_single_quote_is_rejected(self):
        text = "#Class\n사람 'blue'\n"
        result = mg.parse_lst(text)
        self.assertFalse(result.ok)
        self.assertTrue(any("홑따옴표" in e.message for e in result.errors))

    def test_null_url_and_icon_become_none(self):
        text = "#Class\n동물\n\n#Nodes\n보미 동물 보미 null files/Dog.png 2\n"
        result = mg.parse_lst(text)
        node = result.nodes["보미"]
        self.assertIsNone(node.url)
        self.assertEqual(node.icon, "files/Dog.png")
        self.assertEqual(node.display, "2")


class TestVisDataMapping(unittest.TestCase):
    def setUp(self):
        text = (
            "#Class\n사람 blue circle\n\n"
            "#Relation\n"
            "likes 좋아한다 arrow 2\n"
            "isPreviousTo ~보다_먼저이다 sequence\n\n"
            "#Nodes\n철수 사람 철수\n영이 사람 영이\n\n"
            "#Links\n철수 영이 likes\n영이 철수 isPreviousTo\n"
        )
        self.result = mg.parse_lst(text)
        self.assertTrue(self.result.ok)
        self.nodes, self.edges = mg.build_vis_data(self.result)

    def test_class_color_and_shape_applied(self):
        n = next(n for n in self.nodes if n["id"] == "철수")
        self.assertEqual(n["color"], "blue")
        self.assertEqual(n["shape"], "circle")

    def test_relation_display_option_2_shows_description(self):
        e = next(e for e in self.edges if e["from"] == "철수")
        self.assertEqual(e["label"], "좋아한다")
        self.assertEqual(e["title"], "likes")

    def test_sequence_arrow_uses_orange_thick_style(self):
        e = next(e for e in self.edges if e["from"] == "영이")
        self.assertEqual(e["color"], mg.SEQUENCE_COLOR)
        self.assertEqual(e["width"], 4)


if __name__ == "__main__":
    unittest.main()
