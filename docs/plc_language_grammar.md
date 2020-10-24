# Grammar

program ::= {statement}
statement ::= "TASK" taskType identifier nl |
              "ROUTINE" identifier nl |
              "RUNG" identifier nl |
              "RUNG" nl |
              instruction nl |
              "ENDRUNG" nl |
              "ENDROUTINE" nl |
              "ENDTASK" nl |
              "TAG" identifier "=" (true | false) nl
taskType ::= "<" (periodType | eventType) ">"
periodType ::= "PERIOD" "=" number
eventType ::= "EVENT" "=" identifier
instruction ::= ("XIO" | "XIC" | "OTE" | "OTL" | "OTU" | "EMIT" | "JSR") identifier
nl ::= '\n'+
