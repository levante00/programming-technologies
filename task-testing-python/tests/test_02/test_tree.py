from tree_utils_02.tree import Tree, FileNode
import tempfile
import os
import pytest
import shutil


def test_construct_filenode():
    tree = Tree()
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_node = tree.construct_filenode(tmpdirname, True)

        assert isinstance(file_node, FileNode)
        assert file_node.name == os.path.basename(tmpdirname)
        assert file_node.is_dir == True
        assert file_node.children == []

    with tempfile.NamedTemporaryFile() as fp:
        file_size_node = tree.construct_filenode(fp.name, False)

        assert isinstance(file_size_node, FileNode)
        assert file_size_node.name == os.path.basename(fp.name)
        assert file_size_node.is_dir == False
        assert file_size_node.children == []


def test_update_filenode():
    tree = Tree()

    file_node_1 = FileNode("dir_child_1", True, [])
    file_node_2 = FileNode("temp_file", False, [])

    update_filenode_1 = tree.update_filenode(file_node_1)
    update_filenode_2 = tree.update_filenode(file_node_2)

    assert file_node_1 == update_filenode_1
    assert file_node_2 == update_filenode_2


def test_get():
    def get_child(name, parent):
        return list(
            filter(
                lambda child: child.name == os.path.basename(name),
                parent.children,
            )
        )[0]

    tree = Tree()

    with tempfile.NamedTemporaryFile() as fp:
        with pytest.raises(AttributeError) as error:
            assert tree.get(fp.name, True)
        assert str(error.value) == "Path is not directory"

        assert None == tree.get(fp.name, True, True)

        file_node = tree.get(fp.name, False)

        assert isinstance(file_node, FileNode)
        assert file_node.name == os.path.basename(fp.name)
        assert file_node.is_dir == False
        assert file_node.children == []

        file_node = tree.get(fp.name, False)

        assert isinstance(file_node, FileNode)
        assert file_node.name == os.path.basename(fp.name)
        assert file_node.is_dir == False
        assert file_node.children == []

    with tempfile.TemporaryDirectory() as tmpdirname:
        child_dir_1 = tempfile.mkdtemp(dir=tmpdirname)
        child_dir_2 = tempfile.mkdtemp(dir=tmpdirname)
        child_dir_1_1 = tempfile.mkdtemp(dir=child_dir_1)
        child_dir_1_2 = tempfile.mkdtemp(dir=child_dir_1)
        child_dir_2_1 = tempfile.mkdtemp(dir=child_dir_2)

        child_file_1_1 = tempfile.NamedTemporaryFile(dir=tmpdirname)

        file_node_root_1 = tree.get(tmpdirname, True)

        assert isinstance(file_node_root_1, FileNode)
        assert file_node_root_1.name == os.path.basename(tmpdirname)
        assert file_node_root_1.is_dir == True
        assert len(file_node_root_1.children) == 2
        assert (
            len(get_child(os.path.basename(child_dir_1), file_node_root_1).children)
            == 2
        )
        assert (
            len(get_child(os.path.basename(child_dir_2), file_node_root_1).children)
            == 1
        )

        file_node_root_2 = tree.get(tmpdirname, False)

        assert isinstance(file_node_root_2, FileNode)
        assert file_node_root_2.name == os.path.basename(tmpdirname)
        assert file_node_root_2.is_dir == True
        assert len(file_node_root_2.children) == 3
        assert (
            len(get_child(os.path.basename(child_dir_1), file_node_root_2).children)
            == 2
        )
        assert (
            len(get_child(os.path.basename(child_dir_2), file_node_root_2).children)
            == 1
        )
        
        child_file_1_1.close()

    non_existing_path = "non_existing_path"
    non_existing_path_error = "Path not exist"

    with pytest.raises(AttributeError) as error:
        assert tree.get(non_existing_path, False)
    assert str(error.value) == non_existing_path_error

    with pytest.raises(AttributeError) as error:
        assert tree.get(non_existing_path, True)
    assert str(error.value) == non_existing_path_error

    with pytest.raises(AttributeError) as error:
        assert tree.get(non_existing_path, False, True)
    assert str(error.value) == non_existing_path_error

    with pytest.raises(AttributeError) as error:
        assert tree.get(non_existing_path, True, True)
    assert str(error.value) == non_existing_path_error


def test_filter_empty_nodes():
    tree = Tree()

    file_node = FileNode("temp_file", False, [])
    assert None == tree.filter_empty_nodes(file_node)

    file_node = FileNode("temp_dir", True, [])

    with pytest.raises(ValueError) as error:
        assert tree.filter_empty_nodes(file_node)
    assert str(error.value) == "Code should not be executed here!"

    with tempfile.TemporaryDirectory() as tmpdirname:
        child_dir_1 = tempfile.mkdtemp(dir=tmpdirname)
        child_dir_2 = tempfile.mkdtemp(dir=tmpdirname)

        child_node_1 = FileNode(child_dir_1, True, [])
        child_node_2 = FileNode(child_dir_2, True, [])
        root_node = FileNode(tmpdirname, True, [child_node_1, child_node_2])

        tree.filter_empty_nodes(root_node)

        assert os.listdir(tmpdirname) == []
