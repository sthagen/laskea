# Generated from jql.g4 by ANTLR 4.9.3
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .jqlParser import jqlParser
else:
    from jqlParser import jqlParser

# This class defines a complete listener for a parse tree produced by jqlParser.
class jqlListener(ParseTreeListener):

    # Enter a parse tree produced by jqlParser#parse.
    def enterParse(self, ctx: jqlParser.ParseContext):
        pass

    # Exit a parse tree produced by jqlParser#parse.
    def exitParse(self, ctx: jqlParser.ParseContext):
        pass

    # Enter a parse tree produced by jqlParser#jql_stmt_list.
    def enterJql_stmt_list(self, ctx: jqlParser.Jql_stmt_listContext):
        pass

    # Exit a parse tree produced by jqlParser#jql_stmt_list.
    def exitJql_stmt_list(self, ctx: jqlParser.Jql_stmt_listContext):
        pass

    # Enter a parse tree produced by jqlParser#jql_stmt.
    def enterJql_stmt(self, ctx: jqlParser.Jql_stmtContext):
        pass

    # Exit a parse tree produced by jqlParser#jql_stmt.
    def exitJql_stmt(self, ctx: jqlParser.Jql_stmtContext):
        pass

    # Enter a parse tree produced by jqlParser#expr.
    def enterExpr(self, ctx: jqlParser.ExprContext):
        pass

    # Exit a parse tree produced by jqlParser#expr.
    def exitExpr(self, ctx: jqlParser.ExprContext):
        pass

    # Enter a parse tree produced by jqlParser#ordering_term.
    def enterOrdering_term(self, ctx: jqlParser.Ordering_termContext):
        pass

    # Exit a parse tree produced by jqlParser#ordering_term.
    def exitOrdering_term(self, ctx: jqlParser.Ordering_termContext):
        pass

    # Enter a parse tree produced by jqlParser#operator.
    def enterOperator(self, ctx: jqlParser.OperatorContext):
        pass

    # Exit a parse tree produced by jqlParser#operator.
    def exitOperator(self, ctx: jqlParser.OperatorContext):
        pass

    # Enter a parse tree produced by jqlParser#literal_value.
    def enterLiteral_value(self, ctx: jqlParser.Literal_valueContext):
        pass

    # Exit a parse tree produced by jqlParser#literal_value.
    def exitLiteral_value(self, ctx: jqlParser.Literal_valueContext):
        pass

    # Enter a parse tree produced by jqlParser#literal_list.
    def enterLiteral_list(self, ctx: jqlParser.Literal_listContext):
        pass

    # Exit a parse tree produced by jqlParser#literal_list.
    def exitLiteral_list(self, ctx: jqlParser.Literal_listContext):
        pass

    # Enter a parse tree produced by jqlParser#keyword.
    def enterKeyword(self, ctx: jqlParser.KeywordContext):
        pass

    # Exit a parse tree produced by jqlParser#keyword.
    def exitKeyword(self, ctx: jqlParser.KeywordContext):
        pass

    # Enter a parse tree produced by jqlParser#state_name.
    def enterState_name(self, ctx: jqlParser.State_nameContext):
        pass

    # Exit a parse tree produced by jqlParser#state_name.
    def exitState_name(self, ctx: jqlParser.State_nameContext):
        pass

    # Enter a parse tree produced by jqlParser#field.
    def enterField(self, ctx: jqlParser.FieldContext):
        pass

    # Exit a parse tree produced by jqlParser#field.
    def exitField(self, ctx: jqlParser.FieldContext):
        pass

    # Enter a parse tree produced by jqlParser#compare_dates.
    def enterCompare_dates(self, ctx: jqlParser.Compare_datesContext):
        pass

    # Exit a parse tree produced by jqlParser#compare_dates.
    def exitCompare_dates(self, ctx: jqlParser.Compare_datesContext):
        pass

    # Enter a parse tree produced by jqlParser#dates.
    def enterDates(self, ctx: jqlParser.DatesContext):
        pass

    # Exit a parse tree produced by jqlParser#dates.
    def exitDates(self, ctx: jqlParser.DatesContext):
        pass


del jqlParser
