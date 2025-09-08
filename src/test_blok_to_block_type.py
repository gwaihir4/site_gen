import unittest

from markdown_blocks import block_to_block_type,BlockType,markdown_to_blocks

class TestBlockToBlockType(unittest.TestCase):
    def test1(self):
        md_block ="""- This is a list\n- with items a\n- New list element\n-other element"""
        #md_block = markdown_to_blocks(md_block)
        self.assertEqual((block_to_block_type(md_block)),BlockType.UNORDERED_LIST)
    def test2(self):
        md_block ="""1. This is a list\n2. with items a\n3. New list element\n4.other element with order"""
        #md_block = markdown_to_blocks(md_block)
        self.assertEqual((block_to_block_type(md_block)),BlockType.ORDERED_LIST)
    def test3(self):
        md_block ="""``` Code Block ```"""
        #md_block = markdown_to_blocks(md_block)
        self.assertEqual((block_to_block_type(md_block)),BlockType.CODE)
    def test4(self):
        md_block ="""> Quoter\n> Other Quote\n> New Quote\n> lastest Quote"""
        #md_block = markdown_to_blocks(md_block)
        self.assertEqual((block_to_block_type(md_block)),BlockType.QUOTE)
    def test5(self):
        md_block ="""# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6"""
        #md_block = markdown_to_blocks(md_block)
        self.assertEqual((block_to_block_type(md_block)),BlockType.HEADING)
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()