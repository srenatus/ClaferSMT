from ast import Module
from ast import GCard
from ast import Supers
from ast import Clafer
from ast import Exp
from ast import Declaration
from ast import LocalDeclaration
from ast import IRConstraint
from ast import FunExp
from ast import ClaferId
from ast import DeclPExp
from ast import Goal

from ast import IntegerLiteral
from ast import DoubleLiteral
from ast import StringLiteral
def getModule():
	stack = []
	module = Module.Module("")
	stack.append(module)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(19)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c1_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="B"
	uid="c2_B"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(15))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(2))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(14))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="sum", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(19))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(3)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c24_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(3))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c25_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(7))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c27_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("c1_A_sort_0")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("c2_B_sort_0"), LocalDeclaration.LocalDeclaration("c2_B_sort_1")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c33_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c34_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c35_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c36_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c37_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c38_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c39_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c40_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c41_exp", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(28)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c42_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c43_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_1", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c44_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c45_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c46_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(28)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c47_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c48_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c49_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c50_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(13))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c51_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(15))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c52_exp", pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(19))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c53_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c54_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c55_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_1", isTop=True)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c56_exp", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c57_exp", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_1", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c58_exp", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_0", isTop=True)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c59_exp", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c60_exp", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c61_exp", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_0", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c62_exp", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(16))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c63_exp", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(20))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c64_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c65_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c66_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B_sort_1", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c67_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(16))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c68_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(20))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])])])]))]))])])])])]))
	stack[-1].addElement(constraint)
	return module