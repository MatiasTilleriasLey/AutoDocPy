# autoDocPy

**autoDocPy** is a lightweight Neovim plugin written in Python that automatically generates Google-style docstrings for Python functions.  
It detects the function under the cursor and inserts a properly formatted docstring, including function parameters and return types based on type hints.

## ✨ Features

- Activates only in Python (`.py`) files.
- Works based on the cursor position: generates the docstring for the function where your cursor is.
- Automatically detects function parameters and their type hints.
- Inserts docstrings using the **Google Python Style Guide**.
- Lightweight, fast, and easy to integrate into any Neovim setup.

## ⚙️ Installation

Clone this repository directly into your Neovim Python plugin folder:

```bash
git clone https://github.com/MatiasTilleriasLey/AutoDocPy.git ~/.config/nvim/rplugin/python3/autoDocPy
```

Then, inside Neovim, run:

```vim
:UpdateRemotePlugins
```

That’s it! The plugin is now ready to use.  
Open any `.py` file, place the cursor inside a function, and run:

```vim
:AutoDoc
```

## 🔥 Optional: Key Mapping

To map it to a custom key, add this to your `init.vim`:

```vim
augroup AutoDocPyMappings
    autocmd!
    autocmd FileType python nnoremap <buffer> <leader>d :AutoDoc<CR>
augroup END
```

And define your `<leader>` key (optional):

```vim
let mapleader = " "
```

Now just press `<leader>d` inside a Python function to generate the docstring instantly.

## 🎯 Example

Before:

```python
def add(a: int, b: int) -> int:
    return a + b
```

After running `:AutoDoc`:

```python
def add(a: int, b: int) -> int:
    """
    Description of the `add` function.

    Args:
        a (int): description.
        b (int): description.

    Returns:
        int: description.
    """
    return a + b
```

## 📦 Requirements

- Neovim with Python 3 support.
- Python package [`pynvim`](https://pypi.org/project/pynvim/)

Install `pynvim` with:

```bash
pip install pynvim
```

## 📜 License

MIT License.

## 🤝 Contributions

Pull requests, bug reports, and feature suggestions are very welcome!  
Feel free to contribute and help improve **autoDocPy**.

## 💬 Author

Developed by **Matías Bastian Ezequiel Tillerias Ley**.

