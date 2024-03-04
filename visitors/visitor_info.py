import ast
import re
import os
from typing import Dict, Self
from util.util import opCategory, constCategory
from util.util import IDGetter
import db.dbentities as dbentities
from visitors.visitor_db import Visitor_db
from visitors.My_NodeVisitor import NodeVisitor

class Visitor_info(NodeVisitor):

    def getArgsNameConvention(self, namingConventions : Dict):
        nameConvention = ''
        max = 0
        for nc in namingConventions.keys():
            if(namingConventions[nc] > max): 
                max = namingConventions[nc]
                nameConvention = nc
        return nameConvention

    def whatItIs(self, method):
        whatItIs = {'magic' : False, 'private' : False, 'abstract' : False, 'wrapper' : False, 'cached' : False, 'static' : False, 'classmethod' : False, 'property' : False}
        magic_patron = re.compile(r'^__\w+__$')
        private_patron = re.compile(r'^_\w+$')
        whatItIs["magic"] = True if magic_patron.match(method.name) else False
        whatItIs["private"] = True if private_patron.match(method.name) else False
        for decorator in method.decorator_list:
            if(isinstance(decorator,ast.Name)):
                if(decorator.id == "abstractmethod"): whatItIs["abstract"] = True
                if(decorator.id == "wraps"): whatItIs["wrapper"] = True
                if(decorator.id == "cache"): whatItIs["cached"] = True
                if(decorator.id == "staticmethod"): whatItIs["static"] = True
                if(decorator.id == "classmethod"): whatItIs["classmethod"] = True
                if(decorator.id == "property"): whatItIs["property"] = True
        return whatItIs

    def nameConvention(self, name):
        lower_patron = re.compile(r'^[a-z]+$')
        upper_patron = re.compile(r'^[A-Z_]+$')
        camelLow_patron = re.compile(r'^[a-z][a-zA-Z]*$')
        camelUp_patron = re.compile(r'^[A-Z][a-zA-Z]*$')
        snakeCase_patron = re.compile(r'^[a-z_]+$')
        discard_patron = re.compile(r'^_+$')
        if(discard_patron.match(name)): return 'Discard'
        elif(snakeCase_patron.match(name)): return 'SnakeCase'
        elif(upper_patron.match(name)): return 'Upper'
        elif(lower_patron.match(name)): return 'Lower'
        elif(camelLow_patron.match(name)): return 'CamelLow'
        elif(camelUp_patron.match(name)): return 'CamelUp'
        else: 
            return 'NoNameConvention'



    def addParam(self, dict_1 : Dict, param, value):
        new_dict = dict_1.copy()
        new_dict[param] = value
        return new_dict

    def sumMatch(self, dict_1 : Dict, dict_2):
        {
            'matchValue' : dict_1["matchValue"] + dict_2["matchValue"], 
            'matchSingleton' : dict_1["matchSingleton"] + dict_2["matchSingleton"], 
            'matchSequence' : dict_1["matchSequence"] + dict_2["matchSequence"], 
            'matchMapping' : dict_1["matchMapping"] + dict_2["matchMapping"], 
            'matchClass' : dict_1["matchClass"] + dict_2["matchClass"], 
            'matchStar' : dict_1["matchStar"] + dict_2["matchStar"], 
            'matchAs' : dict_1["matchAs"] + dict_2["matchAs"], 
            'matchOr' : dict_1["matchOr"] + dict_2["matchOr"], 
            'depth' : max(dict_1["depth"],dict_2["depth"])
        }

    def __init__(self):
        self.idGetter = IDGetter()
        self.visitor_db = Visitor_db()

    def visit_Program(self: Self, params : Dict):
        dbprogram = dbentities.DBProgram()
        ########## ENTITIE PROPERTIES ############
        numOfDirs = 0
        numOfPackages = 0
        name = params["path"].split("\\")[-1]
        totalClassDefs = 0
        totalFunctionDefs = 0
        totalEnumDefs = 0
        ############## PROPAGAR VISIT ############
        modules = []
        index = 0
        for directorio_actual, subdirectorios, archivos in os.walk(params["path"]):
            """
            if(directorio_actual.split("\\")[-2] == name):
                hasInitPy = False
                hasPy = False
                for archivo in archivos:
                    if archivo == '__init__.py': 
                        hasInitPy = True
                    elif archivo.endswith('.py'):
                        hasPy = True
                if hasInitPy: numOfPackages += 1
                elif hasPy: numOfDirs += 1
            """
            hasInitPy = False
            hasPy = False
            hasCodeRoot = False
            for archivo in archivos:
                if(directorio_actual.split("\\")[-1] != name):
                    if archivo == '__init__.py': 
                        hasInitPy = True
                    elif archivo.endswith('.py'):
                        hasPy = True
                else:
                    if archivo.endswith('.py'): 
                        hasCodeRoot = True
                ruta_completa = os.path.join(directorio_actual, archivo)
                if(archivo.endswith('.py') and not 'MACOSX' in ruta_completa):
                    with open(ruta_completa, "r",  encoding='utf-8') as f:
                        module_ast = None
                        try:
                            contenido = f.read()
                            module_ast = ast.parse(contenido)
                        except Exception as e:
                            # NO COMPILAN
                            pass
                        if module_ast:
                            try:
                                if(len(module_ast.body) > 0):
                                    modules.append(self.visit(module_ast, {"user_id" : params["user_id"], "experticeLevel" : params["experticeLevel"], "filename" : archivo.split('.')[0], "path" : ruta_completa}))
                                    totalClassDefs += modules[index]["classdefs"]
                                    totalEnumDefs += modules[index]["enumDefs"]
                                    totalFunctionDefs += modules[index]["functionDefs"]
                                    index += 1
                            except Exception as e:
                                raise e
                                # NO COMPILAN
                                pass
            if hasInitPy: numOfPackages += 1
            elif hasPy: numOfDirs += 1
        ########## ENTITIE PROPERTIES ############
        if(index > 0):
            totalDefs = totalClassDefs + totalEnumDefs+ totalFunctionDefs
            dbprogram.program_id = self.idGetter.getID()
            dbprogram.numberOfPackages = numOfPackages
            dbprogram.numberOfSubDirsWithCode = numOfDirs
            dbprogram.hasCodeRootPackage = hasCodeRoot
            dbprogram.hasPackages = numOfPackages > 0
            dbprogram.hasSubDirsWithCode = numOfDirs > 0
            dbprogram.numberOfModules = index
            dbprogram.averageDefsPerModule = totalDefs/index
            dbprogram.classDefsPct = totalClassDefs/totalDefs if totalDefs > 0 else 0
            dbprogram.functionDefsPct = totalFunctionDefs/totalDefs if totalDefs > 0 else 0
            dbprogram.enumDefsPct = totalEnumDefs/totalDefs if totalDefs > 0 else 0
        ############## VISITOR DB ################  
            self.visitor_db.visit_Program(dbprogram, {})                
        return

    # params = [parent, parent_id = node]
    def visit_Expr(self: Self, node : ast.Expr, params : Dict):
        return self.visit(node.value, params)

    def visit_Module(self : Self, node : ast.Module , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        module = dbentities.DBModule()
        dbimport = dbentities.DBImport()
        ############ IDS #########################
        id = self.idGetter.getID()
        if(id == 85):
            print(1)
        dbnode.node_id = module.module_id = dbimport.import_id = module.import_id = id
        ############# PARAMS #####################
        childparams = {"parent" : module, "depth" : 1, "parent_id" : id, "role" : "Module"}
        ############## PROPAGAR VISIT ############
        methodCount = 0
        functionsBodySize = 0
        numberOfMethodStmt = 0
        typeAnnotations = 0
        simpleImportNum = 0
        fromImportNum = 0
        localImports = 0
        simpleImportModulesNum = 0
        fromImportModulesNum = 0
        asnames = 0
        hasEntryPoint = False
        count = {'stmt' : 0, 'expr' : 0, 'classes' : 0, 'function' : 0, 'enum' : 0}
        ########## ENTITIE PROPERTIES ############
        returns = []
        fromImports = []
        simpleImports = []
        functions = []
        classes = []
        cindex = 0
        findex = 0
        siindex = 0
        fiindex = 0
        index = 0
        for child in node.body:
            returns.append(self.visit(child, childparams))
            if(isinstance(child,ast.Expr)): count["expr"] += 1
            elif(isinstance(child,ast.ClassDef)): 
                count["classes"] += 1
                classes.append(returns[index])
                numberOfMethodStmt += returns[index]["numberOfMethodStmt"]
                methodCount += returns[index]["methodCount"]
                typeAnnotations += returns[index]["typeAnnotations"]
                cindex += 1
            elif(isinstance(child,ast.FunctionDef) or isinstance(child,ast.AsyncFunctionDef)): 
                count["function"] += 1
                functions.append(returns[index])
                functionsBodySize += returns[index]["function"].bodyCount
                typeAnnotations += returns[index]["typeAnnotations"]
                findex += 1
            #elif(isinstance(child,ast.enum)): count["enum"] += 1 ?
            elif(isinstance(child,ast.Import)): 
                simpleImportNum += 1
                simpleImports.append(returns[index])
                siindex += 1
                simpleImportModulesNum += returns[index]["importedModules"]
                if(siindex + fiindex != index): localImports += 1
            elif(isinstance(child,ast.ImportFrom)):
                fromImportNum += 1
                fromImports.append(returns[index])
                fiindex += 1
                asnames += returns[index]["asnames"]
                fromImportModulesNum += returns[index]["importedModules"]
                if(siindex + fiindex != index): localImports += 1
            elif(isinstance(child,ast.stmt)): count["stmt"] += 1
            if(isinstance(child, ast.If) and not hasEntryPoint):
                if(ast.unparse(child.test) == "__name__ == '__main__'"): hasEntryPoint = True
            index += 1
        ########## ENTITIE PROPERTIES ############
        module.name = params["filename"]
        module.nameConvention = self.nameConvention(module.name)
        module.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        module.globalStmtsPct = count["stmt"]/index if(index > 0) else 0
        module.globalExpressions = count["expr"]/index if(index > 0) else 0
        module.numberOfClasses = count["classes"]
        module.numberOfFunctions = count["function"]
        enumClassFunctSum = (count["function"] + count["enum"] + count["classes"])
        module.classDefsPct = count["classes"]/enumClassFunctSum if(enumClassFunctSum > 0) else 0
        module.functionDefsPct = count["function"]/enumClassFunctSum if(enumClassFunctSum > 0) else 0
        module.enumDefsPct = count["enum"]/enumClassFunctSum if(enumClassFunctSum > 0) else 0
        module.averageStmtsFunctionBody = functionsBodySize/findex if(findex > 0) else 0
        module.averageStmtsMethodBody = numberOfMethodStmt/methodCount if(methodCount > 0) else 0
        module.typeAnnotationsPct = typeAnnotations/(methodCount + findex) if(findex + methodCount > 0) else 0
        module.path = params["path"]
        module.hasEntryPoint = hasEntryPoint
        #------------ imports --------------------
        dbimport.numberImports = (siindex + fiindex)
        dbimport.moduleImportsPct = simpleImportNum/(siindex + fiindex) if(siindex + fiindex > 0) else 0
        dbimport.fromImportsPct = fromImportNum/(siindex + fiindex) if(siindex + fiindex > 0) else 0
        dbimport.localImportsPct = localImports/(siindex + fiindex) if(siindex + fiindex > 0) else 0
        dbimport.averageAsInImportedModules = asnames/fromImportModulesNum if(fromImportModulesNum > 0) else 0
        dbimport.averageImportedModules = simpleImportModulesNum/siindex if(siindex > 0) else 0
        dbimport.averageFromImportedModules = fromImportModulesNum/fiindex if(fiindex > 0) else 0
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : module, 'dbnode' : dbnode, 'dbimport' : dbimport})
        return {"classdefs" : count["classes"], "functionDefs" : count["function"], "enumDefs" : count["enum"]}
    
    def visit_FunctionDef(self : Self, node : ast.FunctionDef , params : Dict) -> Dict: 
        isMethod = params["parent"].table == 'ClassDefs'
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        if(isMethod): method = dbentities.DBMethodDef()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = function.functiondef_id = function.parameters_id = id
        dbnode.parent_id = function.module_id = params["parent_id"]
        if(isMethod):
            method.classdef_id = params["parent_id"]
            method.methoddef_id = id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params["depth"] + 1, "parent_id" : id}
        if(isMethod):
            stmtRoles = ["MethodDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmtRoles = ["FunctionDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfBodyExpr = 0
        depth = 0
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.addParam(self.addParam(childparams, "params_id", id), "role" , "FunctionParams"))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                aux = self.visit(child, self.addParam(childparams,"role", exprRoles[2]))
                numberOfBodyExpr += 1
            else:
                aux = self.visit(child, self.addParam(childparams,"role", stmtRoles[0]))
            depth = max(depth, aux["depth"])
        for child in node.decorator_list:
            self.visit(child, self.addParam(childparams,"role", exprRoles[0]))
        if(node.returns):
            aux = self.visit(node.returns, self.addParam(childparams,"role", exprRoles[1]))
            depth = max(depth, aux["depth"])
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        whatitis = self.whatItIs(node)
        function.nameConvention = self.nameConvention(node.name)
        function.isPrivate = whatitis["private"]
        function.isMagic = whatitis["magic"]
        function.bodyCount = len(node.body)
        function.isAsync = False
        function.numberOfDecorators = len(node.decorator_list)
        function.hasReturnTypeAnnotation = node.returns
        if(node.returns): args["typeAnnotations"] += 1
        function.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        function.height = params["depth"]
        function.typeAnnotationsPct = args["typeAnnotations"]/(args["numberOfArgs"] + 1)
        function.sourceCode = ast.unparse(node)
        if(isMethod):
            method.isClassMethod = whatitis["classmethod"]
            method.isStaticMethod = whatitis["static"]
            method.isConstructorMethod = node.name == '__init__'
            method.isAbstractMethod = whatitis["abstract"]
            method.isProperty = whatitis["property"]
            method.isWrapper = whatitis["wrapper"]
            method.isCached = whatitis["cached"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode})
        if(isMethod):
            return {'method': method, 'function': function, 'args': args, 'typeAnnotations' : args["typeAnnotations"], 'depth' : depth + 1, 'id' : function.functiondef_id}
        else:
            return{'function': function, 'typeAnnotations' : args["typeAnnotations"], 'depth' : depth + 1, 'id' : function.functiondef_id}
    
    def visit_AsyncFunctionDef(self : Self, node : ast.AsyncFunctionDef , params : Dict) -> Dict: 
        isMethod = params["parent"].table == 'ClassDefs'
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        if(isMethod): method = dbentities.DBMethodDef()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = function.functiondef_id = function.parameters_id = id
        dbnode.parent_id = function.module_id = params["parent_id"]
        if(isMethod):
            method.classdef_id = params["parent_id"]
            method.methoddef_id = id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params["depth"] + 1, "parent_id" : id}
        if(isMethod):
            stmtRoles = ["AsyncMethodDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmtRoles = ["AsyncFunctionDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfBodyExpr = 0
        depth = 0
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.addParam(self.addParam(childparams, "params_id", id), "role" , "FunctionParams"))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                aux = self.visit(child, self.addParam(childparams,"role", exprRoles[2]))
                numberOfBodyExpr += 1
            else:
                aux = self.visit(child, self.addParam(childparams,"role", stmtRoles[0]))
            depth = max(depth, aux["depth"])
        for child in node.decorator_list:
            self.visit(child, self.addParam(childparams,"role", exprRoles[0]))
        if(node.returns):
            aux = self.visit(node.returns, self.addParam(childparams,"role", exprRoles[1]))
            depth = max(depth, aux["depth"])
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        whatitis = self.whatItIs(node)
        function.nameConvention = self.nameConvention(node.name)
        function.isPrivate = whatitis["private"]
        function.isMagic = whatitis["magic"]
        function.bodyCount = len(node.body)
        function.isAsync = True
        function.numberOfDecorators = len(node.decorator_list)
        function.hasReturnTypeAnnotation = node.returns
        if(node.returns): args["typeAnnotations"] += 1
        function.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        function.height = params["depth"]
        function.typeAnnotationsPct = args["typeAnnotations"]/(args["numberOfArgs"] + 1)
        function.sourceCode = ast.unparse(node)
        if(isMethod):
            method.isClassMethod = whatitis["classmethod"]
            method.isStaticMethod = whatitis["static"]
            method.isConstructorMethod = node.name == '__init__'
            method.isAbstractMethod = whatitis["abstract"]
            method.isProperty = whatitis["property"]
            method.isWrapper = whatitis["wrapper"]
            method.isCached = whatitis["cached"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode})
        if(isMethod):
            return {'method': method, 'function': function, 'args': args,  'typeAnnotations' : args["typeAnnotations"], 'depth' : depth + 1, 'id' : function.functiondef_id}
        else:
            return{'function': function, 'typeAnnotations' : args["typeAnnotations"], 'depth' : depth + 1, 'id' : function.functiondef_id}
        
    def visit_ClassDef(self : Self, node : ast.ClassDef , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        classdef = dbentities.DBClassDef()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = classdef.classdef_id = id
        dbnode.parent_id = classdef.module_id = params["parent_id"]
        ############# PARAMS #####################
        childparams = {"parent" : classdef, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["ClassDef"]
        exprRoles = ["ClassBase", "ClassDecorator", "ClassBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfMethods = 0
        bodyCount = len(node.body)
        assignmentNumber = 0
        expressionNumber = 0
        metaclassNumber = 0
        keywordNumber = 0
        numberOfMethodStmt = 0
        numberOfPrivateMethods = 0
        numberOfMethodTypeAnnotations = 0
        numberOfMethodParamsRet = 0
        numberOfMagicMethods = 0
        numberOfAsyncMethods = 0
        numberOfClassMethods = 0
        numberOfStaticMethods = 0
        numberOfAbstractMethods = 0
        numberOfPropertyMethods = 0
        depth = 0
        ############## PROPAGAR VISIT ############
        for child in node.bases:
            self.visit(child, self.addParam(childparams,"role", exprRoles[0]))
            if(isinstance(child, ast.Name)): classdef.isEnumClass = (child.id == 'Enum')
            else: classdef.isEnumClass = (child.attr == 'Enum')
        for child in node.keywords:
            if(child.arg == 'metaclass'): metaclassNumber += 1
            else : keywordNumber += 1
            self.visit(child, childparams)
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                expressionNumber += 1
                returns = self.visit(child, self.addParam(childparams,"role", exprRoles[2]))
            else:
                if(isinstance(child, ast.AnnAssign) or isinstance(child, ast.AugAssign) or isinstance(child, ast.Assign)): assignmentNumber += 1
                returns = self.visit(child, self.addParam(childparams,"role", stmtRoles[0]))
                if(isinstance(child,ast.FunctionDef) or isinstance(child,ast.AsyncFunctionDef)):
                    numberOfMethods += 1
                    numberOfMethodStmt += returns["function"].bodyCount
                    numberOfMethodParamsRet += (returns["args"]["numberOfArgs"] + 1)
                    numberOfMethodTypeAnnotations += returns["args"]["typeAnnotations"]
                    if(returns["function"].isMagic): numberOfMagicMethods += 1
                    if(returns["function"].isPrivate): numberOfPrivateMethods += 1
                    if(returns["function"].isAsync): numberOfAsyncMethods += 1
                    if(returns["method"].isAbstractMethod): numberOfAbstractMethods += 1
                    if(returns["method"].isClassMethod): numberOfClassMethods += 1
                    if(returns["method"].isStaticMethod): numberOfStaticMethods += 1
                    if(returns["method"].isProperty): numberOfPropertyMethods += 1
            depth = max(depth, returns["depth"])
        for child in node.decorator_list:
            self.visit(child, self.addParam(childparams,"role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        classdef.nameConvention = self.nameConvention(node.name)
        classdef.numberOfMethods = numberOfMethods
        classdef.numberOfDecorators = len(node.decorator_list)
        classdef.numberOfBaseClasses = len(node.bases)
        classdef.hasGenericTypeAnnotations = len(node.type_params) > 0
        classdef.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        classdef.bodyCount = bodyCount
        classdef.assignmentsPct = assignmentNumber/bodyCount
        classdef.expressionsPct = expressionNumber/bodyCount
        classdef.usesMetaclass = metaclassNumber > 0
        classdef.numberOfKeyWords = keywordNumber
        classdef.height = params["depth"]
        classdef.averageStmtsMethodBody = numberOfMethodStmt/numberOfMethods
        classdef.typeAnnotationsPct = numberOfMethodTypeAnnotations/numberOfMethodParamsRet
        classdef.privateMethodsPct = numberOfPrivateMethods/numberOfMethods
        classdef.magicMethodsPct = numberOfMagicMethods/numberOfMethods
        classdef.asyncMethodsPct = numberOfAsyncMethods/numberOfMethods
        classdef.classMethodsPct = numberOfClassMethods/numberOfMethods
        classdef.staticMethodsPct = numberOfStaticMethods/numberOfMethods
        classdef.abstractMethodsPct = numberOfAbstractMethods/numberOfMethods
        classdef.propertyMethodsPct = numberOfPropertyMethods/numberOfMethods
        classdef.sourceCode = ast.unparse(node)
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : classdef, 'dbnode' : dbnode})
        return {'methodCount' : numberOfMethods, 'typeAnnotations' : numberOfMethodTypeAnnotations, 'numberOfMethodStmt' : numberOfMethodStmt, 'id' : classdef.classdef_id, 'depth' : depth + 1}

    ############################### STATEMENTS #############################

    def visit_Return(self : Self, node : ast.Return , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id, "role" : "Return"}
        ########## ENTITIE PROPERTIES ############
        returns = None
        ############## PROPAGAR VISIT ############
        if(node.value): returns = self.visit(node.value, childparams)
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        if(returns):
            stmt.depth = returns["depth"]
            stmt.first_child_id = returns["id"]
        else:
            stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    def visit_Delete(self : Self, node : ast.Delete , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id, "role" : "Delete"}
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.targets:
            returns.append(self.visit(child, childparams))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    def visit_Assign(self : Self, node : ast.Assign , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "AssignmentStmt"
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        roles = ["AssignLHS", "AssignRHS"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns_targets = []
        index = 0
        for child in node.targets:
            returns_targets.append(self.visit(child, self.addParam(childparams,'role',roles[0])))
            depth = max(depth, returns_targets[index]["depth"])
            if(index == 0): first_child_id = returns_targets[index]["id"]
            if(index == 1): second_child_id = returns_targets[index]["id"]
            if(index == 2): third_child_id = returns_targets[index]["id"]
            index += 1
        returns_value = self.visit(node.value, self.addParam(childparams,'role',roles[1]))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.depth = 0
        stmt.depth = max(returns_value["depth"],depth)
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}
    
    def visit_TypeAlias(self : Self, node : ast.TypeAlias , params : Dict) -> Dict:
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        roles = ["TypeAliasLHS", "TypeAliasRHS"]
        ############## PROPAGAR VISIT ############
        returns = []
        for child in node.type_params:
            self.visit(child, childparams)
        returns.append(self.visit(node.name, self.addParam(childparams,'role', roles[0])))
        returns.append(self.visit(node.value, self.addParam(childparams,'role', roles[1])))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        stmt.first_child_id = returns[0]["id"]
        stmt.second_child_id = returns[1]["id"]
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}
    
    def visit_AugAssign(self : Self, node : ast.AugAssign , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "AugmentedAssignment"
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        roles = ["AugmentedAssigmentLHS", "AugmentedAssigmentRHS"]
        ############## PROPAGAR VISIT ############
        returns = []
        returns.append(self.visit(node.target, self.addParam(childparams,'role', roles[0])))
        returns.append(self.visit(node.value, self.addParam(childparams,'role', roles[1])))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        stmt.first_child_id = returns[0]["id"]
        stmt.second_child_id = returns[1]["id"]
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    def visit_AnnAssign(self : Self, node : ast.AnnAssign , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "AnnotatedAssignment"
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        roles = ["VarDefVarName", "VarDefType", "VarDefInitValue"]
        ############## PROPAGAR VISIT ############
        returns = []
        returns.append(self.visit(node.target, self.addParam(childparams,'role', roles[0])))
        returns.append(self.visit(node.annotation, self.addParam(childparams,'role', roles[1])))
        if(node.value): returns.append(self.visit(node.value, self.addParam(childparams,'role', roles[2])))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        stmt.first_child_id = returns[0]["id"]
        stmt.second_child_id = returns[1]["id"]
        if(returns[2]): 
            stmt.third_child_id = returns[2]["id"]
            stmt.depth = max(stmt.depth, returns[2]["depth"])
        stmt.sourceCode = ast.unparse(node)
        stmt.hasOrElse = None
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    def visit_For(self : Self, node : ast.For , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["For", "ForElse"]
        exprRoles = ["ForElement", "ForEnumerable", "ForBody", "ForElseBody"]
        ########## ENTITIE PROPERTIES ############
        stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_target = self.visit(node.target, self.addParam(childparams,'role', exprRoles[0]))
        returns_iter = self.visit(node.iter, self.addParam(childparams,'role', exprRoles[1]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            stmt.hasOrElse = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[3])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.height = params["depth"]
        stmt.depth = max(returns_target["depth"],max(returns_iter["depth"],depth))
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_AsyncFor(self : Self, node : ast.AsyncFor , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "For"
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["AsyncFor", "AsyncForElse"]
        exprRoles = ["AsyncForElement", "AsyncForEnumerable", "AsyncForBody", "AsyncForElseBody"]
        ########## ENTITIE PROPERTIES ############
        stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_target = self.visit(node.target, self.addParam(childparams,'role', exprRoles[0]))
        returns_iter = self.visit(node.iter, self.addParam(childparams,'role', exprRoles[1]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            stmt.hasOrElse = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[3])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.height = params["depth"]
        stmt.depth = max(returns_target["depth"],max(returns_iter["depth"],depth))
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_While(self : Self, node : ast.While , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["While", "WhileElse"]
        exprRoles = ["WhileCondition", "WhileBody", "WhileElseBody"]
        ########## ENTITIE PROPERTIES ############
        stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_test = self.visit(node.test, self.addParam(childparams,'role', exprRoles[0]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            stmt.hasOrElse = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.height = params["depth"]
        stmt.depth = max(returns_test["depth"],depth)
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}


    def visit_If(self : Self, node : ast.If , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["If", "IfElse"]
        exprRoles = ["IfCondition", "IfBody", "IfElseBody"]
        ########## ENTITIE PROPERTIES ############
        stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_test = self.visit(node.test, self.addParam(childparams,'role', exprRoles[0]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            
                depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        bodySize = index
        for child in node.orelse:
            stmt.hasOrElse = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.height = params["depth"]
        stmt.depth = max(returns_test["depth"],depth)
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = bodySize
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}


    def visit_With(self : Self, node : ast.With , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["With"]
        exprRoles = ["WithElement", "WithAs", "WithBody"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.items:
            self.visit(child, self.addParam(self.addParam(childparams,"role_ctx", exprRoles[0]),'role_vars', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_AsyncWith(self : Self, node : ast.AsyncWith , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["AsyncWith"]
        exprRoles = ["AsyncWithElement", "AsyncWithAs", "AsyncWithBody"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.items:
            self.visit(child, self.addParam(self.addParam(childparams,"role_ctx", exprRoles[0]),'role_vars', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Match(self : Self, node : ast.Match , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        case = dbentities.DBCase()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        subject = self.visit(node.subject, self.addParam(childparams,'role', exprRoles[0]))
        for child in node.cases:
            returns.append(self.visit(child, childparams))
            depth = max(depth, returns[index]["depth"])
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.first_child_id = subject["id"]
        stmt.hasOrElse = None
        stmt.depth = max(depth,subject["depth"])
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        #-----------------------------------------
        numberOfCasesAs = 0
        numberOfCasesOr = 0
        numberOfCasesValue = 0
        numberOfCasesSingleton = 0
        numberOfCasesSequence = 0
        numberOfCasesMapping = 0
        numberOfCasesClass = 0
        numberOfCasesStar = 0
        numberOfGuards = 0
        bodyTotalCount = 0
        for i in range(index):
            numberOfCasesAs += returns[i]["matchAs"]
            numberOfCasesOr += returns[i]["matchOr"]
            numberOfCasesValue += returns[i]["matchValue"]
            numberOfCasesMapping += returns[i]["matchMapping"]
            numberOfCasesClass += returns[i]["matchClass"]
            numberOfCasesSingleton += returns[i]["matchSingleton"]
            numberOfCasesSequence += returns[i]["matchSequence"]
            numberOfCasesStar += returns[i]["matchStar"]
            numberOfGuards += returns[i]["guards"]
            bodyTotalCount += returns[i]["bodyCount"]
        totalCases = numberOfCasesAs + numberOfCasesOr + numberOfCasesMapping + numberOfCasesSequence + numberOfCasesSingleton + numberOfCasesStar + numberOfCasesClass + numberOfCasesValue
        case.numberOfCases = totalCases
        case.guards = numberOfGuards/totalCases
        case.averageBodyCount = bodyTotalCount/index
        case.averageMatchValue = numberOfCasesValue/totalCases
        case.averageMatchSingleton = numberOfCasesSingleton/totalCases
        case.averageMatchSequence = numberOfCasesSequence/totalCases
        case.averageMatchMapping = numberOfCasesMapping/totalCases
        case.averageMatchClass = numberOfCasesClass/totalCases
        case.averageMatchStar = numberOfCasesStar/totalCases
        case.averageMatchAs = numberOfCasesAs/totalCases
        case.averageMatchOr = numberOfCasesOr/totalCases
        case.statement_id = id
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode, 'case': case})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Raise(self : Self, node : ast.Raise , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Raise","RaiseFrom"]
        ########## ENTITIE PROPERTIES ############
        cause = None
        exc = None
        ############## PROPAGAR VISIT ############
        if(node.exc): exc = self.visit(node.exc, self.addParam(childparams,'role', exprRoles[0]))
        if(node.cause): cause = self.visit(node.cause, self.addParam(childparams,'role', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        if(exc):
            stmt.first_child_id = exc["id"]
            if(cause):
                stmt.second_child_id = cause["id"]  
                stmt.depth = max(exc["depth"], cause["depth"])
            else:
                stmt.depth = exc["depth"]
        else:
            if(cause):
                stmt.first_child_id = cause["id"]
                stmt.depth = cause["depth"]
            else:
                stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}
    
    def visit_Try(self : Self, node : ast.Try , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        handler = dbentities.DBHandler()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = handler.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["Try", "TryElse", "TryFinally", "TryHandler"]
        exprRoles = ["TryBody", "TryElse", "FinallyBody"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        handlers = []
        index = 0
        hindex = 0
        handlersBodies = 0
        hasOrElse = False
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[0])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
            hasOrElse = True
        for child in node.finalbody:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[2])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.handlers:
            handlers.append(self.visit(child, self.addParam(self.addParam(childparams,"role", stmtRoles[3]),'handler', handler)))
            depth = max(depth, handlers[hindex]["depth"])
            hindex += 1
            handlersBodies += len(child.body)
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = hasOrElse
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index + handlersBodies
        #--------------- handler -----------------
        handler.numberOfHandlers = index
        if(node.finalbody):
            handler.hasFinally = True
        else:
            handler.hasFinally = False
        handler.hasCatchAll = False
        for child in handlers:
            if(child["isCatchAll"]): handler.hasCatchAll = True
        handler.averageBodyCount = handlersBodies/handler.numberOfHandlers
        handler.hasStar = False
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode, 'handler' : handler})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_TryStar(self : Self, node : ast.TryStar , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        handler = dbentities.DBHandler()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = handler.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "Try"
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        stmtRoles = ["Try", "TryElse", "TryFinally", "TryHandlerStar"]
        exprRoles = ["TryBody", "TryElse", "FinallyBody"]
        ############## PROPAGAR VISIT ############
        returns = []
        handlers = []
        index = 0
        hindex = 0
        hasOrElse = False
        handlersBodies = 0
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[0])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
            hasOrElse = True
        for child in node.finalbody:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.addParam(childparams,"role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.addParam(childparams,"role", stmtRoles[2])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.handlers:
            handlers.append(self.visit(child, self.addParam(self.addParam(childparams,"role", stmtRoles[3]),'handler', handler)))
            depth = max(depth, handlers[hindex]["depth"])
            hindex += 1
            handlersBodies += len(child.body)
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = hasOrElse
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index + handlersBodies
        #--------------- handler -----------------
        handler.numberOfHandlers = index
        if(node.finalbody):
            handler.hasFinally = True
        else:
            handler.hasFinally = False
        handler.hasCatchAll = False
        for child in handlers:
            if(child.isCatchAll): handler.hasCatchAll = True
        handler.averageBodyCount = handlersBodies/handler.numberOfHandlers
        handler.hasStar = True
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode, 'handler' : handler})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Assert(self : Self, node : ast.Assert , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES #######################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["AssertCondition", "AssertMessage"]
        ############## PROPAGAR VISIT ############
        test = self.visit(node.test, self.addParam(childparams,'role', exprRoles[0]))
        if(node.msg): msg = self.visit(node.msg, self.addParam(childparams,'role', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.first_child_id = test.id
        stmt.depth = test.depth
        if(msg):
            stmt.second_child_id = msg.id  
            stmt.depth = max(msg.depth, stmt.depth)
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Global(self : Self, node : ast.Global , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Nonlocal(self : Self, node : ast.Nonlocal , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Pass(self : Self, node : ast.Pass , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Break(self : Self, node : ast.Break , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    
    def visit_Continue(self : Self, node : ast.Continue , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : stmt.depth + 1}

    ############################ IMPORTS ##################################

    
    def visit_Import(self : Self, node : ast.Import , params : Dict) -> Dict: 
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        stmt.statement_id = id
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        asnames = 0
        for alias in node.names:
            if(alias.asname): asnames += 1
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt})
        return {'id' : id, 'depth' : stmt.depth + 1, 'importedModules' : len(node.names), 'asnames' : asnames}

    
    def visit_ImportFrom(self : Self, node : ast.ImportFrom , params : Dict) -> Dict: 
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = self.idGetter.getID()
        stmt.statement_id = id
        ########## ENTITIE PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        asnames = 0
        for alias in node.names:
            if(alias.asname): asnames += 1
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : stmt})
        return {'id' : id, 'depth' : stmt.depth + 1, 'importedModules' : len(node.names), 'asnames' : asnames}

    ############################ EXPRESSIONS ##################################

    def visit_BoolOp(self : Self, node : ast.BoolOp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Logical"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Logical"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        self.visit(node.op, childparams)
        for child in node.values:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_NamedExpr(self : Self, node : ast.NamedExpr , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES #######################
        expr.category = "AssignmentExp"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["AssignExpLHS", "AssignExpRHS"]
        ############## PROPAGAR VISIT ############
        target = self.visit(node.target, self.addParam(childparams,'role', exprRoles[0]))
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = target["category"]
        expr.second_child_category = value["category"]
        expr.first_child_id = target["id"]
        expr.second_child_id = value["id"]
        expr.depth = max(target["depth"], value["depth"])
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_BinOp(self : Self, node : ast.BinOp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = opCategory(node)
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Arithmetic", "Shift", "Pow", "MatMult", "BWLogical"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, childparams)
        match node.op:
            case ast.MatMult: role = exprRoles[3]
            case ast.LShift, ast.RShift: role = exprRoles[1]
            case ast.Pow: role = exprRoles[2]
            case ast.BitAnd, ast.BitOr, ast.BitXor: role = exprRoles[4]
            case default: role = exprRoles[0]
        left = self.visit(node.left, self.addParam(childparams,'role', role))
        right = self.visit(node.right, self.addParam(childparams,'role', role))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = left["category"]
        expr.second_child_category = right["category"]
        expr.first_child_id = left["id"]
        expr.second_child_id = right["id"]
        expr.depth = max(left["depth"], right["depth"])
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}
    
    
    def visit_UnaryOp(self : Self, node : ast.UnaryOp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = opCategory(node)
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Arithmetic"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, childparams)
        operand = self.visit(node.operand, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = operand["category"]
        expr.first_child_id = operand["id"]
        expr.depth = operand["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}
    
    
    def visit_Lambda(self : Self, node : ast.Lambda , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["LambdaBody"]
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.addParam(self.addParam(childparams, "params_id", id), "role", "LambdaParams"))
        aux = self.visit(node.body, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = aux["category"]
        expr.first_child_id = aux["id"]
        expr.depth = aux["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}
    
    
    def visit_IfExp(self : Self, node : ast.IfExp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Ternary"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############ PARAMS ######################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["TernaryCondition", "TernaryIfBody", "TernaryElseBody"]
        ############## PROPAGAR VISIT ############
        test = self.visit(node.test, self.addParam(childparams,'role', exprRoles[0]))
        body = self.visit(node.body, self.addParam(childparams,'role', exprRoles[1]))
        orelse = self.visit(node.orelse, self.addParam(childparams,'role', exprRoles[2]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = test["category"]
        expr.second_child_category = body["category"]
        expr.third_child_category = orelse["category"]
        expr.first_child_id = test["id"]
        expr.second_child_id = body["id"]
        expr.third_child_id = orelse["id"]
        expr.depth = max(max(body["depth"],orelse["depth"]),test["depth"])
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ######################### COMPREHENSIONS #############################

    
    def visit_ListComp(self : Self, node : ast.ListComp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "ListComprehension"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, childparams))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_SetComp(self : Self, node : ast.SetComp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "SetComprehension"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, childparams))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_DictComp(self : Self, node : ast.DictComp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "DictComprehension"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        third_child_category = None
        fourth_child_category = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, childparams))
            if(index == 0): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 1): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        key = self.visit(node.key, self.addParam(childparams,'role', exprRoles[0]))
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = key["category"]
        expr.second_child_category = value["category"]
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = key["id"]
        expr.second_child_id = value["id"]
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(max(key.depth, value["depth"]), depth)
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_GeneratorExp(self : Self, node : ast.GeneratorExp , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "GeneratorComprehension"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, childparams))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ######################################################################

    
    def visit_Await(self : Self, node : ast.Await , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Await"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Yield(self : Self, node : ast.Yield , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Yield"]
        ############## PROPAGAR VISIT ############
        if(node.value): value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        if(value):
            expr.first_child_category = value["category"]
            expr.first_child_id = value["id"]
            expr.depth = value["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_YieldFrom(self : Self, node : ast.YieldFrom , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["YieldFrom"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Compare(self : Self, node : ast.Compare , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Compare", "Relational", "Is", "In"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        left = self.visit(node.left, self.addParam(childparams,'role', exprRoles[0]))
        index = 0
        returns = []
        for child in node.comparators:
            match node.ops[index]:
                case ast.Is, ast.IsNot: returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[2])))
                case ast.In: returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[3])))
                case default: returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(left["depth"], depth)
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ########################## call_args ###########################

    
    def visit_Call(self : Self, node : ast.Call , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        callArgs = dbentities.DBCallArg()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = callArgs.expression_id = id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["CallFuncName", "CallArg"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        namedArgs = 0
        staredArgs = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.args:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            index += 1
        func = self.visit(node.func, self.addParam(childparams,'role', exprRoles[0]))
        for child in node.keywords:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(child.arg): namedArgs += 1
            if('**' in ast.unparse(child.value)): staredArgs += 1
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(func["depth"], depth)
        #------------- CallArgs ------------------
        callArgs.numberArgs = index
        callArgs.namedArgsPct = namedArgs/callArgs.numberArgs if callArgs.numberArgs > 0 else 0
        callArgs.doubleStarArgsPct = staredArgs/callArgs.numberArgs  if callArgs.numberArgs > 0 else 0
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : callArgs, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ################################################################

    def visit_FormattedValue(self : Self, node : ast.FormattedValue , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["FormattedValue", "FormattedFormat"]
        ########## ENTITIE PROPERTIES ############
        spec = None
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        if(node.format_spec): spec = self.visit(node.format_spec, self.addParam(childparams,'role', exprRoles[1]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        if(spec):
            expr.second_child_category = spec["category"]
            expr.second_child_id = spec["id"]
            expr.depth = max(spec["depth"], expr.depth)
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ########################### F-strings #####################################

    
    def visit_JoinedStr(self : Self, node : ast.JoinedStr , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        fstr = dbentities.DBFString()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = fstr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "FString"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["FString"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.values:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : fstr, 'dbnode' : dbnode, 'expr' : expr})
        return  {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ###########################################################################

    
    def visit_Constant(self : Self, node : ast.Constant , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = constCategory(node)
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return  {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Attribute(self : Self, node : ast.Attribute , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Dot"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Dot"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Subscript(self : Self, node : ast.Subscript , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Indexing"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Slice", "Indexing"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[1]))
        slice = self.visit(node.slice, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.second_child_category = slice["category"]
        expr.first_child_id = value["id"]
        expr.second_child_id = slice["id"]
        expr.depth = max(slice["depth"],value["depth"])
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Starred(self : Self, node : ast.Starred , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Star"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Star"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ############################# Variable ##################################

    
    def visit_Name(self : Self, node : ast.Name , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        var = dbentities.DBVariable()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = var.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Variable"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        #------------- VARIABLE ------------------
        var.numberOfCharacters = len(node.id)
        var.nameConvention = self.nameConvention(node.id)
        var.isPrivate = False
        var.isMagic = False
        if(node.id.startswith('_')):
            if(node.id.endswith('_')):
                var.isMagic = True
            else:
                var.isPrivate = True
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : var, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ############################### Vectors #################################

    
    def visit_List(self : Self, node : ast.List , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "ListLiteral"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["ListLiteral"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(homogeneous and type(child) != lastType): lastType = False
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Tuple(self : Self, node : ast.Tuple , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "TupleLiteral"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["TupleLiteral"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(homogeneous and type(child) != lastType): lastType = False
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Dict(self : Self, node : ast.Dict , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "DictionaryLiteral"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.keys:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            index += 1
        for child in node.values:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(homogeneous and type(child) != lastType): lastType = False
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.keys)
        vct.homogeneous = homogeneous
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    
    def visit_Set(self : Self, node : ast.Set , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "SetLiteral"
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["SetLiteral"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(homogeneous and type(child) != lastType): lastType = False
            index += 1
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ########################################################################

    
    def visit_Slice(self : Self, node : ast.Slice , params : Dict) -> Dict: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = self.idGetter.getID()
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params["depth"] + 1, "parent_id" : id}
        exprRoles = ["Slice"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        step = None
        lower = None
        upper = None
        ############## PROPAGAR VISIT ############
        if(node.lower):
            lower = self.visit(node.lower, self.addParam(childparams,'role', exprRoles[0]))
            depth = max(depth, lower["depth"])
        if(node.upper):
            upper = self.visit(node.upper, self.addParam(childparams,'role', exprRoles[0]))
            depth = max(depth, upper["depth"])
        if(node.step):
            step = self.visit(node.step, self.addParam(childparams,'role', exprRoles[0]))
            depth = max(depth, step["depth"])
        ########## ENTITIE PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        if(lower): 
            expr.first_child_category = lower["category"]
            expr.first_child_id = lower["id"]
            if(upper):        
                expr.second_child_category = upper["category"]
                expr.second_child_id = upper["id"]
                if(step):
                    expr.third_child_category = step["category"]
                    expr.third_child_id = step["id"]
            else:
                if(step):
                    expr.second_child_category = step["category"]
                    expr.second_child_id = step["id"]
        else:
            if(upper):        
                expr.first_child_category = upper["category"]
                expr.first_child_id = upper["id"]
                if(step):
                    expr.second_child_category = step["category"]
                    expr.second_child_id = step["id"]
            else:
                if(step):
                    expr.first_child_category = step["category"]
                    expr.first_child_id = step["id"]
        expr.depth = depth
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return {'id' : id, 'depth' : expr.depth + 1, 'category' : expr.category}

    ############################### Cases ###################################

    
    def visit_MatchValue(self : Self, node : ast.MatchValue , params : Dict) -> Dict: 
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, self.addParam(childparams,'role', exprRoles[0]))
        return {'matchValue' : 1, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 1}

    
    def visit_MatchSingleton(self : Self, node : ast.MatchSingleton , params : Dict) -> Dict: 
        return {'matchValue' : 0, 'matchSingleton' : 1, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 1}

    
    def visit_MatchSequence(self : Self, node : ast.MatchSequence , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 1, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 0}
        ############## PROPAGAR VISIT ############
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, childparams))
            index += 1
            returns = self.sumMatch(returns,childs[index])
        returns["depth"] += 1
        return returns

    
    def visit_MatchMapping(self : Self, node : ast.MatchMapping , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        exprRoles = ["MatchCondition"]
        ################ RETURNS #################
        returns = {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 1, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 0}
        ############## PROPAGAR VISIT ############
        childs = []
        exprs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, childparams))
            index += 1
            returns = self.sumMatch(returns,childs[index])
        index = 0
        for child in node.keys:
            exprs.append(self.visit(child, self.addParam(childparams,'role', exprRoles[0])))
            returns["depth"] = max(returns["depth"], exprs[index]["depth"])
            index += 1
        returns["depth"] += 1
        return returns

    
    def visit_MatchClass(self : Self, node : ast.MatchClass , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        exprRoles = ["MatchCondition"]
        ################ RETURNS #################
        returns = {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 1, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 1}
        ############## PROPAGAR VISIT ############
        cls = self.visit(node.cls, self.addParam(childparams,'role', exprRoles[0]))
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, childparams))
            index += 1
            returns = self.sumMatch(returns,childs[index])
        for child in node.kwd_patterns:
            childs.append(self.visit(child, childparams))
            index += 1
            returns = self.sumMatch(returns,childs[index])
        returns["depth"] = max(returns["depth"] + 1, cls["depth"])
        return returns

    
    def visit_MatchStar(self : Self, node : ast.MatchStar , params : Dict) -> Dict: 
        return {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 1, 'matchAs' : 0, 'matchOr' : 0, 'depth' : 1}

    
    def visit_MatchAs(self : Self, node : ast.MatchAs , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 1, 'matchOr' : 0, 'depth' : 1}
        ############## PROPAGAR VISIT ############
        if(node.pattern): child = self.visit(node.pattern, childparams)
        returns["depth"] = max(returns["depth"], child["depth"] + 1)
        return returns

    
    def visit_MatchOr(self : Self, node : ast.MatchOr , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue' : 0, 'matchSingleton' : 0, 'matchSequence' : 0, 'matchMapping' : 0, 'matchClass' : 0, 'matchStar' : 0, 'matchAs' : 0, 'matchOr' : 1, 'depth' : 1}
        ############## PROPAGAR VISIT ############
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, childparams))
            index += 1
            returns = self.sumMatch(returns,childs[index])
        returns["depth"] += 1
        return returns
    
    ############################# HANDLER ####################################

    def visit_ExceptHandler(self : Self, node : ast.ExceptHandler , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["handler"], "depth" : params["depth"] + 1, "parent_id" : params["parent_id"]}
        exprRoles = ["ExceptType", "ExceptBody"]
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        depth = 0
        isCatchAll = True
        if(node.type): 
            self.visit(node.type, self.addParam(childparams,'role', exprRoles[0]))
            isCatchAll = False
        for child in node.body:
            returns.append(self.visit(child, self.addParam(childparams,'role', exprRoles[1])))
            depth = max(depth,returns[index]["depth"])
            index += 1
        return { 'id' : params["parent_id"], 'depth' : depth, 'isCatchAll' : isCatchAll}

    ####################### Visits extra ######################

    def visit_comprehension(self : Self, node : ast.comprehension , params : Dict) -> Dict: 
        ############# PARAMS #####################
        exprRoles = ["ComprehensionTarget", "ComprehensionIter", "ComprehensionIf"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        target = self.visit(node.target, self.addParam(params,'role', exprRoles[0]))
        iter = self.visit(node.iter, self.addParam(params,'role', exprRoles[1]))
        for child in node.ifs:
            returns.append(self.visit(child, self.addParam(params,'role', exprRoles[2])))
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITIE PROPERTIES ############
        depth = max(max(target["depth"], iter["depth"]), depth)
        return {'id' : params["parent_id"], 'category' : params["parent"].category, 'depth' : depth + 1}
    
    def visit_arguments(self : Self, node : ast.arguments , params : Dict) -> Dict: 
        dbparams = dbentities.DBParameter()
        ############### IDS ######################
        dbparams.parameters_id = params["params_id"]
        dbparams.parent_id = params["parent_id"]
        ############## ROLES #####################
        dbparams.parametersRole = params["role"]
        ############# PARAMS #####################
        exprRoles = ["DefaultParamValue"]
        ########## ENTITIE PROPERTIES ############
        numberOfAnnotations = 0
        numberOfParams = 0
        nameConvention = ''
        namingConventions = {'CamelUp' : 0, 'CamelLow' : 0, 'SnakeCase' : 0, 'Discard' : 0, 'Upper' : 0, 'Lower' : 0, 'NoNameConvention' : 0 }
        ############## PROPAGAR VISIT ############
        for child in node.posonlyargs:
            arg = self.visit(child, params)
            if(arg["typeAnnotation"]): numberOfAnnotations += 1
            numberOfParams += 1
            namingConventions[self.nameConvention(child.arg)] += 1
        for child in node.args:
            arg =  self.visit(child, params)
            if(arg["typeAnnotation"]): numberOfAnnotations += 1
            numberOfParams += 1
            namingConventions[self.nameConvention(child.arg)] += 1
        if(node.vararg): 
            arg =  self.visit(node.vararg, params)
            if(arg["typeAnnotation"]): numberOfAnnotations += 1
            numberOfParams += 1
            namingConventions[self.nameConvention(child.arg)] += 1
        for child in node.kwonlyargs:
            arg =  self.visit(child, params)
            if(arg["typeAnnotation"]): numberOfAnnotations += 1
            numberOfParams += 1
            namingConventions[self.nameConvention(child.arg)] += 1
        for child in node.kw_defaults:
            self.visit(child, self.addParam(params,'role', exprRoles[0]))
        if(node.kwarg):
            arg = self.visit(node.kwarg, params)
            if(arg["typeAnnotation"]): numberOfAnnotations += 1
            numberOfParams += 1
            namingConventions[self.nameConvention(child.arg)] += 1
        for child in node.defaults:
            self.visit(child, self.addParam(params,'role', exprRoles[0]))
        ########## ENTITIE PROPERTIES ############
        dbparams.nameConvention = self.getArgsNameConvention(namingConventions)
        dbparams.numberOfParams = numberOfParams
        dbparams.posOnlyParamPct = len(node.posonlyargs)
        dbparams.varParamPct = (1 if node.vararg else 0)/numberOfParams if numberOfParams > 0 else 0
        dbparams.hasVarParam = True if node.vararg else False
        dbparams.typeAnnotationPct = numberOfAnnotations/numberOfParams if numberOfParams > 0 else 0
        dbparams.kwOnlyParamPct = len(node.kwonlyargs)/numberOfParams if numberOfParams > 0 else 0
        dbparams.defaultValuePct = (len(node.kw_defaults) + len(node.defaults))/numberOfParams if numberOfParams > 0 else 0
        dbparams.hasKWParam = True if node.kwarg else False
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {"dbparams" : dbparams})
        return {"typeAnnotations" : numberOfAnnotations, "numberOfArgs" : numberOfParams}
    
    def visit_arg(self : Self, node : ast.arg , params : Dict) -> Dict:
        ############# PARAMS ##################### 
        exprRoles = ["TypeAnnotation"]
        ############## PROPAGAR VISIT ############
        if(node.annotation): 
            self.visit(node.annotation, self.addParam(params,'role', exprRoles[0]))
            return {'typeAnnotation' : True}
        return {'typeAnnotation' : False}
    
    def visit_keyword(self : Self, node : ast.keyword , params : Dict) -> Dict: 
        ############## PROPAGAR VISIT ############
        return self.visit(node.value, params)
    
    def visit_withitem(self : Self, node : ast.withitem , params : Dict) -> Dict: 
        ############# PARAMS #####################
        childparams = {"parent" : params["parent"], "depth" : params["depth"], "parent_id" : params["parent_id"]}
        ############## PROPAGAR VISIT ############
        self.visit(node.context_expr, self.addParam(childparams, 'role', params["role_ctx"]))
        if(node.optional_vars): self.visit(node.optional_vars, self.addParam(childparams,'role', params["role_vars"]))
        return
    
    def visit_match_case(self : Self, node : ast.match_case , params : Dict) -> Dict: 
        ############# PARAMS #####################
        stmtRoles = ["Case"]
        exprRoles = ["CaseGuard", "CaseBody"]
        ########## ENTITIE PROPERTIES ############
        depth = 0
        ############## PROPAGAR VISIT ############
        childs = []
        index = 0
        returns = self.visit(node.pattern, params)
        guards = 0
        if(node.guard): 
            guard = self.visit(node.guard, self.addParam(params,'role', exprRoles[0]))
            guards = 1
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                childs.append(self.visit(child, self.addParam(params,"role", exprRoles[1])))
            else:
                childs.append(self.visit(child, self.addParam(params,"role", stmtRoles[0])))
            index += 1
        ########## ENTITIE PROPERTIES ############
        for i in range(index):
            depth = max(depth, childs[i]["depth"])
        returns = self.addParam(returns,'guards',guards)
        returns = self.addParam(returns,'bodyCount',index)
        return returns
    
    def visit_TypeVar(self : Self, node : ast.TypeVar , params : Dict) -> Dict: 
        ############# PARAMS #####################
        exprRoles = ["TypeVar"]
        ############## PROPAGAR VISIT ############
        if(node.bound): self.visit(node.bound, self.addParam(params,'role', exprRoles[0]))
        return
    
    def visit_ParamSpec(self : Self, node : ast.ParamSpec , params : Dict) -> Dict: 
        return
    
    def visit_TypeVarTuple(self : Self, node : ast.TypeVarTuple , params : Dict) -> Dict: 
        return
    
    ###########################################################
    