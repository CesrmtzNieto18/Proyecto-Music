// Generated from /home/cesar/Documentos/Zamora5/Zamora5/AUTOMATAS1/APPMUSIC/Bazilio.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link BazilioParser}.
 */
public interface BazilioListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link BazilioParser#programa}.
	 * @param ctx the parse tree
	 */
	void enterPrograma(BazilioParser.ProgramaContext ctx);
	/**
	 * Exit a parse tree produced by {@link BazilioParser#programa}.
	 * @param ctx the parse tree
	 */
	void exitPrograma(BazilioParser.ProgramaContext ctx);
	/**
	 * Enter a parse tree produced by {@link BazilioParser#procedimiento}.
	 * @param ctx the parse tree
	 */
	void enterProcedimiento(BazilioParser.ProcedimientoContext ctx);
	/**
	 * Exit a parse tree produced by {@link BazilioParser#procedimiento}.
	 * @param ctx the parse tree
	 */
	void exitProcedimiento(BazilioParser.ProcedimientoContext ctx);
	/**
	 * Enter a parse tree produced by {@link BazilioParser#bloque}.
	 * @param ctx the parse tree
	 */
	void enterBloque(BazilioParser.BloqueContext ctx);
	/**
	 * Exit a parse tree produced by {@link BazilioParser#bloque}.
	 * @param ctx the parse tree
	 */
	void exitBloque(BazilioParser.BloqueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Asignacion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterAsignacion(BazilioParser.AsignacionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Asignacion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitAsignacion(BazilioParser.AsignacionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Lectura}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterLectura(BazilioParser.LecturaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Lectura}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitLectura(BazilioParser.LecturaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Escritura}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterEscritura(BazilioParser.EscrituraContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Escritura}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitEscritura(BazilioParser.EscrituraContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Reproduccion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterReproduccion(BazilioParser.ReproduccionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Reproduccion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitReproduccion(BazilioParser.ReproduccionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Invocacion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterInvocacion(BazilioParser.InvocacionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Invocacion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitInvocacion(BazilioParser.InvocacionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Condicional}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterCondicional(BazilioParser.CondicionalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Condicional}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitCondicional(BazilioParser.CondicionalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Iteracion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterIteracion(BazilioParser.IteracionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Iteracion}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitIteracion(BazilioParser.IteracionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Agregado}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterAgregado(BazilioParser.AgregadoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Agregado}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitAgregado(BazilioParser.AgregadoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Corte}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterCorte(BazilioParser.CorteContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Corte}
	 * labeled alternative in {@link BazilioParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitCorte(BazilioParser.CorteContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Indice}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIndice(BazilioParser.IndiceContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Indice}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIndice(BazilioParser.IndiceContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Lista}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterLista(BazilioParser.ListaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Lista}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitLista(BazilioParser.ListaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Variable}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterVariable(BazilioParser.VariableContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Variable}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitVariable(BazilioParser.VariableContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Relacional}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterRelacional(BazilioParser.RelacionalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Relacional}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitRelacional(BazilioParser.RelacionalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Entero}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterEntero(BazilioParser.EnteroContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Entero}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitEntero(BazilioParser.EnteroContext ctx);
	/**
	 * Enter a parse tree produced by the {@code MulDiv}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMulDiv(BazilioParser.MulDivContext ctx);
	/**
	 * Exit a parse tree produced by the {@code MulDiv}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMulDiv(BazilioParser.MulDivContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Parentesis}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParentesis(BazilioParser.ParentesisContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Parentesis}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParentesis(BazilioParser.ParentesisContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Longitud}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterLongitud(BazilioParser.LongitudContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Longitud}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitLongitud(BazilioParser.LongitudContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Nota}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNota(BazilioParser.NotaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Nota}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNota(BazilioParser.NotaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Igualdad}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIgualdad(BazilioParser.IgualdadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Igualdad}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIgualdad(BazilioParser.IgualdadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SumaResta}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterSumaResta(BazilioParser.SumaRestaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SumaResta}
	 * labeled alternative in {@link BazilioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitSumaResta(BazilioParser.SumaRestaContext ctx);
}