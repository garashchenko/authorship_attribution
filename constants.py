from typed_ast import ast27
keywords_dict = [
    {
        "name": "and",
        "ast_class": ast27.And
    },
    {
        "name": "assert",
        "ast_class": ast27.Assert
    },
    {
        "name": "break",
        "ast_class": ast27.Break
    },
    {
        "name": "class",
        "ast_class": ast27.ClassDef
    },
    {
        "name": "continue",
        "ast_class": ast27.Continue
    },
    {
        "name": "def",
        "ast_class": ast27.FunctionDef
    },
    {
        "name": "elif",
        "ast_class": ast27.If,
        "condition": lambda node: len(node.orelse) > 0 and node.orelse[0].__class__ == ast27.If
    },
    {
        "name": "else",
        "ast_class": ast27.If,
        "condition": lambda node: len(node.orelse) > 0 and node.orelse[0].__class__ != ast27.If
    },
    {
        "name": "except",
        "ast_class": ast27.ExceptHandler
    },
    {
        "name": "finally",
        "ast_class": ast27.TryFinally
    },
    {
        "name": "for",
        "ast_class": ast27.For
    },
    {
        "name": "from",
        "ast_class": ast27.ImportFrom
    },
    {
        "name": "global",
        "ast_class": ast27.Global
    },
    {
        "name": "if",
        "ast_class": ast27.If,
        "condition": lambda node: False if len(node.orelse) > 0 and node.orelse[0].__class__ == ast27.If else True
    },
    {
        "name": "import",
        "ast_class": ast27.Import
    },
    {
        "name": "in",
        "ast_class": ast27.In
    },
    {
        "name": "is",
        "ast_class": ast27.Is
    },
    {
        "name": "lambda",
        "ast_class": ast27.Lambda
    },
    # {
    #     "name": "nonlocal",
    #     "ast_class": ast27.Nonlocal
    # },
    {
        "name": "not",
        "ast_class": ast27.Not
    },
    {
        "name": "or",
        "ast_class": ast27.Or
    },
    {
        "name": "pass",
        "ast_class": ast27.Pass
    },
    {
        "name": "raise",
        "ast_class": ast27.Raise
    },
    {
        "name": "return",
        "ast_class": ast27.Return
    },
    {
        "name": "try",
        "ast_class": ast27.TryExcept
    },
    {
        "name": "while",
        "ast_class": ast27.While
    },
    {
        "name": "with",
        "ast_class": ast27.With
    },
    {
        "name": "yield",
        "ast_class": ast27.Yield
    }
]