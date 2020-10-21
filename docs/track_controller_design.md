# Track Controller Design Notes

## Keywords
- TAG - Used to allocate a boolean in the program's memory
- TASK/ENDTASK - A set of routines that can either be periodically run or event-driven
- PERIOD - Option to have a task run at a certain period. Should be followed by an = and an integer.
- EVENT - Option to have a task run when a given event is emitted.
- ROUTINE/ENDROUTINE - A set of sequential ladder rungs containing instructions. The routine keyword must be followed by a string representing the name of the routine. Every task must contain a singular routine named "Main"
- RUNG/ENDRUNG - A list of instructions to be evaluated when the routine runs. Rungs may have a name, or remain anonymous. Starts with entry instructions followed by output instructions
- FALSE
- TRUE
- XIC (Examine if closed) - Continues evaluating the rung if the given tag is true
- XIO (Examine if open) - Continues evaluating the run if the given tag is false
- OTE (Output energize) - Sets the given tag to true while being executed
- OTL (Output latch) - Sets the given tag to true until the an otu instruction is executed
- OTU (Output unlatch) - Sets the given tag to false until an otl or ote instruction is executed
- JSR (Jump to subroutine) - Jumps to a given subroutine
- RET (Return) - Returns from a subroutine to the previously executed jsr instruction
- EMIT - Emits a signal to trigger any event driven tasks

## File format
- All tags should be defined at the top of the file and include their name, default value, and a semicolon
- All rungs must be enclosed in a routine
- All routines must be enclosed in a task
- Instructions within a rung must start with entry instructions (xic and xio) then output instructions (ote, otl, otu, etc.)
- Instructions should end with a semicolon
  
## Other notes
- Rungs are executed sequentially in the order they are written
- A task begins execution in the Main routine. Other routines run when a jsr instruction is executed
- Routines other than the Main routine end when either the last rung is executed or when a ret instruction is executed

## Example PLC file

```
tag switch1 = false;
tag signal1 = false;
tag output1 = false;
tag output2 = false;

TASK<period=1000> EverySecondTask
    ROUTINE Main
        RUNG
            XIC signal1;
            OTL output1;
        ENDRUNG
        RUNG
            XIO signal1;
            OTU output1;
        ENDRUNG
        RUNG
            XIC switch1;
            JSR secondRoutine;
        ENDRUNG
        RUNG
            XIO switch1;
            EVENT MyEvent;
        ENDRUNG
    ENDROUTINE

    ROUTINE secondRoutine
        RUNG
            OTL output2;
            RET;
        ENDRUNG
    ENDROUTINE
ENDTASK

TASK<event=MyEvent>
    ROUTINE Main
        RUNG
            OTU output2;
        ENDRUNG
    ENDROUTINE
ENDTASK

```