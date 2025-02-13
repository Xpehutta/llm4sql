import sqlglot
import sqlglot.expressions as exp
from Levenshtein import distance as levenshtein_distance
from collections import defaultdict

class SQLSimilarity:
    def __init__(self):
        # Use a specific dialect (e.g., 'mysql') or None for auto-detection
        self.dialect = None  # Or 'mysql', 'postgres', 'snowflake', etc.
        
    def normalize_query(self, query):
        """Normalize SQL query: Remove aliases, literals, standardize formatting"""
        try:
            # Parse with auto-detected dialect
            parsed = sqlglot.parse_one(query, read=self.dialect)
            
            # Remove aliases and literals
            parsed = parsed.transform(self._remove_aliases_and_literals)
            
            # Convert to standardized format using the `sql()` method
            normalized = parsed.sql(pretty=True)
            return normalized
        except Exception as e:
            print(f"Normalization error: {e}")
            return None
    
    def ast_similarity(self, query1, query2):
        """Compare AST structures using Levenshtein distance"""
        try:
            parsed1 = sqlglot.parse_one(query1, read=self.dialect)
            parsed2 = sqlglot.parse_one(query2, read=self.dialect)
            
            str1 = self._ast_to_string(parsed1)
            str2 = self._ast_to_string(parsed2)
            
            max_len = max(len(str1), len(str2), 1)
            return 1 - levenshtein_distance(str1, str2) / max_len
        except Exception as e:
            print(f"AST comparison error: {e}")
            return 0
    
    def component_similarity(self, query1, query2):
        """Compare individual query components using Jaccard similarity"""
        components1 = self._extract_components(query1)
        components2 = self._extract_components(query2)
        
        scores = {}
        for key in components1.keys() | components2.keys():
            set1 = set(components1.get(key, []))
            set2 = set(components2.get(key, []))
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            scores[key] = intersection / union if union != 0 else 0
            
        return scores
    
    def _extract_components(self, query):
        """Extract key components from SQL query"""
        components = defaultdict(list)
        try:
            parsed = sqlglot.parse_one(query, read=self.dialect)
            for node in parsed.walk():
                if isinstance(node, exp.Column):
                    components["columns"].append(node.name.lower())
                elif isinstance(node, exp.Table):
                    components["tables"].append(node.name.lower())
                elif isinstance(node, exp.Where):
                    components["conditions"].append(node.sql().lower())
        except Exception as e:
            print(f"Component extraction error: {e}")
        return components
    
    def _ast_to_string(self, node):
        """Convert AST to comparable string representation"""
        return " ".join([str(e.__class__.__name__) for e in node.walk()])

    # Helper function for normalization
    def _remove_aliases_and_literals(self, node):
        """
        Remove aliases and replace literals with a placeholder ('?').
        """
        if isinstance(node, exp.Alias):
            # Remove alias by returning the underlying expression
            return node.this
        if isinstance(node, exp.Literal):
            # Replace all literals with a placeholder ('?')
            return exp.Literal(this="?", is_string=False)  # Use a generic placeholder
        return node
