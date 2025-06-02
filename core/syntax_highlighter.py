from pygments import highlight
from pygments.lexers import PowerShellLexer, BatchLexer
from pygments.formatters import HtmlFormatter
from PyQt6.Qsci import QsciLexerBatch, QsciLexerCustom
from PyQt6.QtGui import QColor, QFont


class PowerShellHighlighter(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
    
    def language(self):
        return "PowerShell"
    
    def description(self, style):
        if style == 0:
            return "Default"
        elif style == 1:
            return "Comment"
        elif style == 2:
            return "String"
        elif style == 3:
            return "Keyword"
        elif style == 4:
            return "Variable"
        elif style == 5:
            return "Number"
        elif style == 6:
            return "Operator"
        elif style == 7:
            return "Cmdlet"
        return ""
    
    def styleText(self, start, end):
        # Simple PowerShell syntax highlighting
        # This is a basic implementation - you can enhance it later
        editor = self.parent()
        if editor is None:
            return
        
        text = editor.text()[start:end]
        self.startStyling(start)
        
        # Basic tokenization
        i = 0
        while i < len(text):
            ch = text[i]
            
            # Comments
            if ch == '#':
                j = i
                while j < len(text) and text[j] != '\n':
                    j += 1
                self.setStyling(j - i, 1)
                i = j
                continue
            
            # Strings
            elif ch in ['"', "'"]:
                quote = ch
                j = i + 1
                while j < len(text) and text[j] != quote:
                    if text[j] == '\\' and j + 1 < len(text):
                        j += 2
                    else:
                        j += 1
                if j < len(text):
                    j += 1
                self.setStyling(j - i, 2)
                i = j
                continue
            
            # Variables
            elif ch == '$':
                j = i + 1
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                self.setStyling(j - i, 4)
                i = j
                continue
            
            # Numbers
            elif ch.isdigit():
                j = i
                while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                    j += 1
                self.setStyling(j - i, 5)
                i = j
                continue
            
            # Default
            else:
                self.setStyling(1, 0)
                i += 1
    
    def setup_styles(self):
        # VS Code PowerShell theme colors
        self.setDefaultPaper(QColor("#1e1e1e"))
        self.setDefaultColor(QColor("#d4d4d4"))
        
        # Style 0: Default
        self.setColor(QColor("#d4d4d4"), 0)
        self.setFont(QFont("Consolas", 10), 0)
        
        # Style 1: Comment
        self.setColor(QColor("#6a9955"), 1)
        self.setFont(QFont("Consolas", 10), 1)
        
        # Style 2: String
        self.setColor(QColor("#ce9178"), 2)
        self.setFont(QFont("Consolas", 10), 2)
        
        # Style 3: Keyword
        self.setColor(QColor("#569cd6"), 3)
        self.setFont(QFont("Consolas", 10, QFont.Weight.Bold), 3)
        
        # Style 4: Variable
        self.setColor(QColor("#9cdcfe"), 4)
        self.setFont(QFont("Consolas", 10), 4)
        
        # Style 5: Number
        self.setColor(QColor("#b5cea8"), 5)
        self.setFont(QFont("Consolas", 10), 5)
        
        # Style 6: Operator
        self.setColor(QColor("#d4d4d4"), 6)
        self.setFont(QFont("Consolas", 10), 6)
        
        # Style 7: Cmdlet
        self.setColor(QColor("#dcdcaa"), 7)
        self.setFont(QFont("Consolas", 10), 7)


class BatchHighlighter(QsciLexerBatch):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_colors()
    
    def setup_colors(self):
        # VS Code Batch theme colors
        self.setDefaultPaper(QColor("#1e1e1e"))
        self.setDefaultColor(QColor("#d4d4d4"))
        
        # Keywords
        self.setColor(QColor("#569cd6"), QsciLexerBatch.Keyword)
        self.setFont(QFont("Consolas", 10, QFont.Weight.Bold), QsciLexerBatch.Keyword)
        
        # Comments
        self.setColor(QColor("#6a9955"), QsciLexerBatch.Comment)
        
        # Labels
        self.setColor(QColor("#dcdcaa"), QsciLexerBatch.Label)
        
        # Variables
        self.setColor(QColor("#9cdcfe"), QsciLexerBatch.Variable)
        
        # Operators
        self.setColor(QColor("#d4d4d4"), QsciLexerBatch.Operator)


class SyntaxHighlighterFactory:
    @staticmethod
    def get_highlighter(file_type: str, parent=None):
        if file_type == "ps1":
            return PowerShellHighlighter(parent)
        elif file_type == "bat":
            return BatchHighlighter(parent)
        else:
            return None
    
    @staticmethod
    def get_lexer(file_type: str):
        if file_type == "ps1":
            return PowerShellLexer()
        elif file_type == "bat":
            return BatchLexer()
        else:
            return None