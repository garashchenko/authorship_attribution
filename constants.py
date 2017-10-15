from typed_ast import ast27, ast3

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
        "name": "not in",
        "ast_class": ast27.NotIn
    },
    {
        "name": "is not",
        "ast_class": ast27.IsNot
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

keywords_dict3 = [
    {
        "name": "and",
        "ast_class": ast3.And
    },
    {
        "name": "assert",
        "ast_class": ast3.Assert
    },
    {
        "name": "break",
        "ast_class": ast3.Break
    },
    {
        "name": "class",
        "ast_class": ast3.ClassDef
    },
    {
        "name": "continue",
        "ast_class": ast3.Continue
    },
    {
        "name": "def",
        "ast_class": ast3.FunctionDef
    },
    {
        "name": "elif",
        "ast_class": ast3.If,
        "condition": lambda node: len(node.orelse) > 0 and node.orelse[0].__class__ == ast3.If
    },
    {
        "name": "else",
        "ast_class": ast3.If,
        "condition": lambda node: len(node.orelse) > 0 and node.orelse[0].__class__ != ast3.If
    },
    {
        "name": "except",
        "ast_class": ast3.ExceptHandler
    },
    {
        "name": "finally",
        "ast_class": ast3.Try,
        "condition": lambda node: hasattr(node, 'finalbody') and len(node.finalbody) > 0
    },
    {
        "name": "for",
        "ast_class": ast3.For
    },
    {
        "name": "from",
        "ast_class": ast3.ImportFrom
    },
    {
        "name": "global",
        "ast_class": ast3.Global
    },
    {
        "name": "if",
        "ast_class": ast3.If,
        "condition": lambda node: False if len(node.orelse) > 0 and node.orelse[0].__class__ == ast27.If else True
    },
    {
        "name": "import",
        "ast_class": ast3.Import
    },
    {
        "name": "in",
        "ast_class": ast3.In
    },
    {
        "name": "not in",
        "ast_class": ast3.NotIn
    },
    {
        "name": "is not",
        "ast_class": ast3.IsNot
    },
    {
        "name": "is",
        "ast_class": ast3.Is
    },
    {
        "name": "lambda",
        "ast_class": ast3.Lambda
    },
    # {
    #     "name": "nonlocal",
    #     "ast_class": ast27.Nonlocal
    # },
    {
        "name": "not",
        "ast_class": ast3.Not
    },
    {
        "name": "or",
        "ast_class": ast3.Or
    },
    {
        "name": "pass",
        "ast_class": ast3.Pass
    },
    {
        "name": "raise",
        "ast_class": ast3.Raise
    },
    {
        "name": "return",
        "ast_class": ast3.Return
    },
    {
        "name": "try",
        "ast_class": ast3.Try
    },
    {
        "name": "while",
        "ast_class": ast3.While
    },
    {
        "name": "with",
        "ast_class": ast3.With
    },
    {
        "name": "yield",
        "ast_class": ast3.Yield
    }
]

terms_ast27 = (
    ast27.Module,
    ast27.Interactive,
    ast27.Expression,
    ast27.FunctionType,
    ast27.Suite,
    ast27.FunctionDef,
    ast27.ClassDef,
    ast27.Return,
    ast27.Delete,
    ast27.Assign,
    ast27.AugAssign,
    ast27.For,
    ast27.While,
    ast27.If,
    ast27.With,
    ast27.Raise,
    ast27.TryExcept,
    ast27.Assert,
    ast27.Import,
    ast27.ImportFrom,
    ast27.Global,
    ast27.Expr,
    ast27.Pass,
    ast27.Break,
    ast27.Continue,
    ast27.BoolOp,
    ast27.BinOp,
    ast27.UnaryOp,
    ast27.Lambda,
    ast27.IfExp,
    ast27.Dict,
    ast27.Set,
    ast27.ListComp,
    ast27.SetComp,
    ast27.DictComp,
    ast27.GeneratorExp,
    ast27.Yield,
    ast27.Compare,
    ast27.Call,
    ast27.Num,
    ast27.Str,
    ast27.Attribute,
    ast27.Subscript,
    ast27.Name,
    ast27.List,
    ast27.Tuple,
    ast27.Load,
    ast27.Store,
    ast27.Del,
    ast27.AugLoad,
    ast27.AugStore,
    ast27.Param,
    ast27.Ellipsis,
    ast27.Slice,
    ast27.ExtSlice,
    ast27.Index,
    ast27.And,
    ast27.Or,
    ast27.Add,
    ast27.Sub,
    ast27.Mult,
    ast27.Div,
    ast27.Mod,
    ast27.Pow,
    ast27.LShift,
    ast27.RShift,
    ast27.BitOr,
    ast27.BitXor,
    ast27.BitAnd,
    ast27.FloorDiv,
    ast27.Invert,
    ast27.Not,
    ast27.UAdd,
    ast27.USub,
    ast27.Eq,
    ast27.NotEq,
    ast27.Lt,
    ast27.LtE,
    ast27.Gt,
    ast27.GtE,
    ast27.Is,
    ast27.IsNot,
    ast27.In,
    ast27.NotIn
)

terms_ast3 = (
    ast3.Module,
    ast3.Interactive,
    ast3.Expression,
    ast3.FunctionType,
    ast3.Suite,
    ast3.FunctionDef,
    ast3.ClassDef,
    ast3.Return,
    ast3.Delete,
    ast3.Assign,
    ast3.AugAssign,
    ast3.For,
    ast3.While,
    ast3.If,
    ast3.With,
    ast3.Raise,
    ast3.Try,
    ast3.Assert,
    ast3.Import,
    ast3.ImportFrom,
    ast3.Global,
    ast3.Expr,
    ast3.Pass,
    ast3.Break,
    ast3.Continue,
    ast3.BoolOp,
    ast3.BinOp,
    ast3.UnaryOp,
    ast3.Lambda,
    ast3.IfExp,
    ast3.Dict,
    ast3.Set,
    ast3.ListComp,
    ast3.SetComp,
    ast3.DictComp,
    ast3.GeneratorExp,
    ast3.Yield,
    ast3.Compare,
    ast3.Call,
    ast3.Num,
    ast3.Str,
    ast3.Attribute,
    ast3.Subscript,
    ast3.Name,
    ast3.List,
    ast3.Tuple,
    ast3.Load,
    ast3.Store,
    ast3.Del,
    ast3.AugLoad,
    ast3.AugStore,
    ast3.Param,
    ast3.Ellipsis,
    ast3.Slice,
    ast3.ExtSlice,
    ast3.Index,
    ast3.And,
    ast3.Or,
    ast3.Add,
    ast3.Sub,
    ast3.Mult,
    ast3.Div,
    ast3.Mod,
    ast3.Pow,
    ast3.LShift,
    ast3.RShift,
    ast3.BitOr,
    ast3.BitXor,
    ast3.BitAnd,
    ast3.FloorDiv,
    ast3.Invert,
    ast3.Not,
    ast3.UAdd,
    ast3.USub,
    ast3.Eq,
    ast3.NotEq,
    ast3.Lt,
    ast3.LtE,
    ast3.Gt,
    ast3.GtE,
    ast3.Is,
    ast3.IsNot,
    ast3.In,
    ast3.NotIn
)