# Track Controller Design Notes

## Keywords
- tag - Used to allocate a boolean in the program's memory
- task - A set of routines that can either be continuously run, periodically run, or event-driven
- continuous - Option to have a task run continuously
- period - Option to have a task run at a certain period. Should be followed by an = and an integer. A period of 0 is equivalent to a continuous task
- event - Option to have a task run when a given event is emitted.
- routine - A set of sequential ladder rungs containing instructions. The routine keyword must be followed by a string representing the name of the routine. Every task must contain a singular routine named "Main"
- rung - A list of instructions to be evaluated when the routine runs. Rungs may have a name, or remain anonymous. Starts with entry instructions followed by output instructions
- false
- true

- xic (Examine if closed) - Continues evaluating the rung if the given tag is true
- xio (Examine if open) - Continues evaluating the run if the given tag is false
- ote (Output energize) - Sets the given tag to true while being executed
- otl (Output latch) - Sets the given tag to true until the an otu instruction is executed
- otu (Output unlatch) - Sets the given tag to false until an otl or ote instruction is executed
- jsr (Jump to subroutine) - Jumps to a given subroutine
- ret (Return) - Returns from a subroutine to the previously executed jsr instruction
- event - Emits a signal to trigger any event driven tasks

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


task<continuous> ContinuousTask
{
    routine Main
    {
        rung
        {
            xic switch1;
            ote signal1;
        }

        rung
        {

        }
    }

    routine secondRoutine
    {

    }
}

task<period=1000> EverySecondTask
{
    routine Main
    {
        rung
        {

        }
    }

    routine secondRoutine
    {

    }
}

task<event=MyEvent>
{
    routine Main
    {
        rung
        {

        }
    }
}

```