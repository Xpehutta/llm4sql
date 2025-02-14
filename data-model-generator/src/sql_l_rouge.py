import re

class SQLRougeL:
    @staticmethod
    def _sql_tokenizer(sql_query):
        """
        Tokenizes an SQL query into meaningful components.
        """
        sql_query = sql_query.strip().lower()
        sql_query = re.sub(r'\s+', ' ', sql_query)

        keyword_pattern = r'\b(select|from|where|join|on|group by|order by|limit|insert|update|and|or|between|delete)\b'
        identifier_pattern = r'[a-z_][a-z0-9_]*'
        operator_pattern = r'[\=\>\<\!\*\+\-\%\&\|]'
        punctuation_pattern = r'[;,\(\)]'

        token_pattern = f'({keyword_pattern}|{identifier_pattern}|{operator_pattern}|{punctuation_pattern})'
        tokens = re.findall(token_pattern, sql_query)
        return tokens

    @staticmethod
    def _lcs(X, Y):
        """
        Computes the length of the Longest Common Subsequence (LCS) between two sequences.
        """
        m = len(X)
        n = len(Y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if X[i - 1] == Y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def rouge_l_sql(self, generated_query, reference_query):
        """
        Computes the ROUGE-L-SQL score between a generated SQL query and a reference SQL query.
        """
        gen_tokens = self._sql_tokenizer(generated_query)
        ref_tokens = self._sql_tokenizer(reference_query)

        lcs_length = self._lcs(gen_tokens, ref_tokens)

        precision = lcs_length / len(gen_tokens) if len(gen_tokens) > 0 else 0
        recall = lcs_length / len(ref_tokens) if len(ref_tokens) > 0 else 0

        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
        
# Example usage:
# sql_rouge = SQLRougeL()
# generated_query = "SELECT customer_id, name FROM customers WHERE email = 'example@example.com'"
# reference_query = "select customer_id , name from customers where email = 'example@example.com'"
# result = sql_rouge.rouge_l_sql(generated_query, reference_query)
# print(result)
