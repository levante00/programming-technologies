from tree_utils_02.size_tree import SizeTree, FileSizeNode
import tempfile
import os


def test_construct_filenode():
    size_tree = SizeTree()
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_size_node = size_tree.construct_filenode(tmpdirname, True)

        assert isinstance(file_size_node, FileSizeNode)
        assert file_size_node.name == os.path.basename(tmpdirname)
        assert file_size_node.is_dir == True
        assert file_size_node.size == 4096
        assert file_size_node.children == []

    with tempfile.NamedTemporaryFile() as fp:
        file_size_node = size_tree.construct_filenode(fp.name, False)

        assert isinstance(file_size_node, FileSizeNode)
        assert file_size_node.name == os.path.basename(fp.name)
        assert file_size_node.is_dir == False
        assert file_size_node.size == os.stat(fp.name).st_size
        assert file_size_node.children == []


def test_update_filenode():
    size_tree = SizeTree()

    file_child_1_child_1 = FileSizeNode("file_child_1_child_1", False, [], 300)
    file_child_1_child_2 = FileSizeNode("file_child_1_child_2", False, [], 400)
    dir_1 = FileSizeNode(
        "dir_child_1", True, [file_child_1_child_1, file_child_1_child_2], 4096
    )

    file_2 = FileSizeNode("temp_file", False, [], 600)

    update_filenode_1 = size_tree.update_filenode(dir_1)
    update_filenode_2 = size_tree.update_filenode(file_2)

    assert 300 + 400 + 4096 == update_filenode_1.size
    assert 600 == update_filenode_2.size
