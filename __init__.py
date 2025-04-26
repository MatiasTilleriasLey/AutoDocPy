import ast
import pynvim

@pynvim.plugin
class AutoDoc(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("AutoDoc", nargs=0)
    def insert_docstring_at_cursor(self):
        buf = self.nvim.current.buffer
        filename = self.nvim.eval("expand('%:t')")
        if not filename.endswith(".py"):
            self.nvim.out_write("This command only works with .py files.\n")
            return

        source = "\n".join(buf[:])
        cursor_row = self.nvim.current.window.cursor[0]

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            self.nvim.out_write(f"Syntax error detected: {e}\n")
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')])

                if start <= cursor_row <= end:
                    if ast.get_docstring(node):
                        self.nvim.out_write("Function already has a docstring.\n")
                        return

                    base_indent = " " * node.col_offset
                    inner_indent = base_indent + " " * 4  # +4 spaces inside the function

                    doc_lines = [f'{inner_indent}"""',
                                 f'{inner_indent}Description of the `{node.name}` function.',
                                 f'{inner_indent}']

                    args_doc = []
                    for arg in node.args.args:
                        if arg.arg == "self":
                            continue
                        tipo = self._get_annotation(arg.annotation)
                        args_doc.append(f'{inner_indent}    {arg.arg} ({tipo}): description.')

                    if args_doc:
                        doc_lines.append(f'{inner_indent}Args:')
                        doc_lines += args_doc
                        doc_lines.append(f'{inner_indent}')

                    if node.returns:
                        return_type = self._get_annotation(node.returns)
                        doc_lines.append(f'{inner_indent}Returns:')
                        doc_lines.append(f'{inner_indent}    {return_type}: description.')
                    else:
                        doc_lines.append(f'{inner_indent}Returns:')
                        doc_lines.append(f'{inner_indent}    type: description.')

                    doc_lines.append(f'{inner_indent}"""')

                    insertion_line = node.lineno
                    buf[insertion_line:insertion_line] = doc_lines
                    self.nvim.out_write("Docstring (Google Style) inserted successfully.\n")
                    return

        self.nvim.out_write("Cursor is not inside a function.\n")

    def _get_annotation(self, annotation: str,hola):
        if annotation is None:
            return "Any"
        elif isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            value = self._get_annotation(annotation.value)
            slice_ = self._get_annotation(annotation.slice)
            return f"{value}[{slice_}]"
        elif isinstance(annotation, ast.Tuple):
            return ", ".join([self._get_annotation(e) for e in annotation.elts])
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_annotation(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        return "Any"

