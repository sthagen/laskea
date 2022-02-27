# Generated from jql.g4 by ANTLR 4.9.3
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .jqlParser import jqlParser
else:
    from jqlParser import jqlParser

# This class defines a complete generic visitor for a parse tree produced by jqlParser.


class jqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by jqlParser#parse.
    def visitParse(self, ctx: jqlParser.ParseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#jql_stmt_list.
    def visitJql_stmt_list(self, ctx: jqlParser.Jql_stmt_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#jql_stmt.
    def visitJql_stmt(self, ctx: jqlParser.Jql_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#expr.
    def visitExpr(self, ctx: jqlParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#ordering_term.
    def visitOrdering_term(self, ctx: jqlParser.Ordering_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#operator.
    def visitOperator(self, ctx: jqlParser.OperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#literal_value.
    def visitLiteral_value(self, ctx: jqlParser.Literal_valueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#literal_list.
    def visitLiteral_list(self, ctx: jqlParser.Literal_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#keyword.
    def visitKeyword(self, ctx: jqlParser.KeywordContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#state_name.
    def visitState_name(self, ctx: jqlParser.State_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#field.
    def visitField(self, ctx: jqlParser.FieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#compare_dates.
    def visitCompare_dates(self, ctx: jqlParser.Compare_datesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by jqlParser#dates.
    def visitDates(self, ctx: jqlParser.DatesContext):
        return self.visitChildren(ctx)


del jqlParser
