import java.lang.System;

class Sample {
    public static void main(String argv[]) throws java.io.IOException {
	Yylex yy = new Yylex(System.in);
	Yytoken t;
	while ((t = yy.yylex()) != null)
	    System.out.println(t);
    }
}

class Utility {
  public static void assert
    (
     boolean expr
     )
      { 
	if (false == expr) {
	  throw (new Error("Error: Assertion failed."));
	}
      }
  
  private static final String errorMsg[] = {
    "Error: Unmatched end-of-comment punctuation.",
    "Error: Unmatched start-of-comment punctuation.",
    "Error: Unclosed string.",
    "Error: Illegal character."
    };
  
  public static final int E_ENDCOMMENT = 0; 
  public static final int E_STARTCOMMENT = 1; 
  public static final int E_UNCLOSEDSTR = 2; 
  public static final int E_UNMATCHED = 3; 

  public static void error
    (
     int code
     )
      {
	System.out.println(errorMsg[code]);
      }
}

class Yytoken {
  Yytoken 
    (
     int index,
     String text,
     int line,
     int charBegin,
     int charEnd
     )
      {
	m_index = index;
	m_text = new String(text);
	m_line = line;
	m_charBegin = charBegin;
	m_charEnd = charEnd;
      }

  public int m_index;
  public String m_text;
  public int m_line;
  public int m_charBegin;
  public int m_charEnd;
  public String toString() {
      return "Token #"+m_index+": "+m_text+" (line "+m_line+")";
  }
}

%%

%{
  private int comment_count = 0;
%} 
%line
%char
%state COMMENT

ALPHA=[A-Za-z]
DIGIT=[0-9]
NONNEWLINE_WHITE_SPACE_CHAR=[\ \t\b\012]
WHITE_SPACE_CHAR=[\n\ \t\b\012]
STRING_TEXT=(\\\"|[^\n\"]|\\{WHITE_SPACE_CHAR}+\\)*
COMMENT_TEXT=([^/*\n]|[^*\n]"/"[^*\n]|[^/\n]"*"[^/\n]|"*"[^/\n]|"/"[^*\n])*


%% 

<YYINITIAL> "," { return (new Yytoken(0,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> ":" { return (new Yytoken(1,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> ";" { return (new Yytoken(2,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "(" { return (new Yytoken(3,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> ")" { return (new Yytoken(4,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "[" { return (new Yytoken(5,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "]" { return (new Yytoken(6,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "{" { return (new Yytoken(7,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "}" { return (new Yytoken(8,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "." { return (new Yytoken(9,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "+" { return (new Yytoken(10,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "-" { return (new Yytoken(11,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "*" { return (new Yytoken(12,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "/" { return (new Yytoken(13,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "=" { return (new Yytoken(14,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "<>" { return (new Yytoken(15,yytext(),yyline,yychar,yychar+2)); }
<YYINITIAL> "<"  { return (new Yytoken(16,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "<=" { return (new Yytoken(17,yytext(),yyline,yychar,yychar+2)); }
<YYINITIAL> ">"  { return (new Yytoken(18,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> ">=" { return (new Yytoken(19,yytext(),yyline,yychar,yychar+2)); }
<YYINITIAL> "&"  { return (new Yytoken(20,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> "|"  { return (new Yytoken(21,yytext(),yyline,yychar,yychar+1)); }
<YYINITIAL> ":=" { return (new Yytoken(22,yytext(),yyline,yychar,yychar+2)); }

<YYINITIAL> {NONNEWLINE_WHITE_SPACE_CHAR}+ { }

<YYINITIAL,COMMENT> \n { }

<YYINITIAL> "/*" { yybegin(COMMENT); comment_count = comment_count + 1; }

<COMMENT> "/*" { comment_count = comment_count + 1; }
<COMMENT> "*/" { 
	comment_count = comment_count - 1; 
	Utility.assert(comment_count >= 0);
	if (comment_count == 0) {
    		yybegin(YYINITIAL);
	}
}
<COMMENT> {COMMENT_TEXT} { }

<YYINITIAL> \"{STRING_TEXT}\" {
	String str =  yytext().substring(1,yytext().length() - 1);
	
	Utility.assert(str.length() == yytext().length() - 2);
	return (new Yytoken(40,str,yyline,yychar,yychar + str.length()));
}
<YYINITIAL> \"{STRING_TEXT} {
	String str =  yytext().substring(1,yytext().length());

	Utility.error(Utility.E_UNCLOSEDSTR);
	Utility.assert(str.length() == yytext().length() - 1);
	return (new Yytoken(41,str,yyline,yychar,yychar + str.length()));
} 
<YYINITIAL> {DIGIT}+ { 
	return (new Yytoken(42,yytext(),yyline,yychar,yychar + yytext().length()));
}	
<YYINITIAL> {ALPHA}({ALPHA}|{DIGIT}|_)* {
	return (new Yytoken(43,yytext(),yyline,yychar,yychar + yytext().length()));
}	
<YYINITIAL,COMMENT> . {
        System.out.println("Illegal character: <" + yytext() + ">");
	Utility.error(Utility.E_UNMATCHED);
}







