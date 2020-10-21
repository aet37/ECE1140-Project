# Class Diagram

```plantuml
@startuml

class HWTrackController::RequestManager
{
    + void HandleRequest(Request&, Response&)
    - void AddRequest(Request&)
    - Request* GetNextRequest()
    - ServiceQueue<Request*> m_requestQueue
}

class Communications << (N,#FFFFFF) Namespace >>
{
    - RequestCode ParseCode(String&)
    - String ParseData(String&)
    - void SendResponse(ResponseCode, char*)
    - void GetTagValue(String&)
    - void SetTagValue(String&)
    - void CreateTag(String&)
    - void StartDownload()
    - void EndDownload()
    - void CreateTask(char*, TaskType)
    - void CreateRoutine(char*)
    - void CreateRung(char*)
    + void CommsTask(void*)
}

class Io << (N, #FFFFFF) Namespace >>
{
    + void SetDisplayText(String&)
    + void SetOutput(int, bool)
    + void IoTask(void*)
    + void InterruptHandler()
}

package "PLC Program"
{

class UserProgram
{
    + void AddTask(Task*)
    + void ClearMemory()
    + bool GetRunMode()
    + void SetRunMode(bool)
    - List<Task*> m_tasks
    - bool m_runMode
    - char* m_pProgramName
}

class Task
{
    {static} + void Run(void*)
    + void Run()
    + void AddRoutine(Routine*)
    - TaskType m_type
    - char* m_pTaskName
    - List<Routine*> m_routineList
}

class Routine
{
    + void Run()
    + void AppendRung(Rung*)
    - char* m_pRoutineName
    - List<Rung*> m_rungList
}

class Rung
{
    + void AddInstruction(Instruction*)
    + void Execute()
    - List<Instruction*> m_instructions
}

class Instruction
{
    + bool Evaluate()
    - InstructionType m_type
    - String m_argument
}

class TagDatabase <<(N,0xFFFFFF) Namespace>>
{
    + void AddTag(char*)
    + bool SetTag(String&, bool)
    + bool GetTagValue(String&, bool&)
    + void DeleteAllTags()
    {static} - HashMap<bool> tags
}

}

Rung *-- "0..*" Instruction : Has
Routine *-- "0..*" Rung : Has
Task *-- "1..*" Routine : Has
UserProgram *-- "0..*" Task : Has

TagDatabase -left- Communications : < Uses
TagDatabase -down- Io : < Uses

TagDatabase - Instruction : < Uses

note bottom of Communications
CommsTask interacts with the serial
port to interface with the software
end note

note right of Io
These functions will interact with
the input/output pins
end note

@enduml
```

# Sequence Diagrams
- Download program
- Programmer manually flips switch
- CTC sends switch position

```plantuml
@startuml

title Program Download
Participant Serial
participant Communications as comms
participant TagDatabase as td
participant UserProgram as up
participant Rung
participant Routine
participant Task

activate comms
[-> Serial : write(DOWNLOAD_START)
comms -> Serial ++ : readline()
return message
comms -> comms : StartDownload()
activate comms
comms -> td : DeleteAllTags()
comms -> up : ClearMemory()
return

[-> Serial : write(CREATE_TAG, "switch1")
comms -> Serial ++ : readline()
return message
comms -> comms : CreateTag()
activate comms
comms -> td : AddTag("switch1")
return

[-> Serial : write(CREATE_RUNG, "XIC Switch1")
comms -> Serial ++ : readline()
return message
comms -> comms : CreateRung("XIC Switch1")
activate comms
comms -> Rung ** : pRung = Rung("XIC Switch1")
return

[-> Serial : write(CREATE_ROUTINE, "Main")
comms -> Serial ++ : readline()
return message
comms -> comms : CreateRoutine("Main")
activate comms
comms -> Routine ** : pRoutine = Routine("Main")
comms -> Routine : AppendRung(pRung)
return

[-> Serial : write(CREATE_TASK, "Task1", PERIODIC)
comms -> Serial ++ : readline()
return message
comms -> comms : CreateTask("Task1", PERIODIC)
activate comms
comms -> Task ** : pTask = Task("Task1", PERIODIC)
comms -> Task : AddRoutine(pRoutine)
comms -> up : AddTask(pTask)
return

[-> Serial : write(END_DOWNLOAD)
comms -> Serial ++ : readline()
return message
comms -> comms : EndDownload()
activate comms
comms -> up : SetRunMode(true)
return
@enduml
```

```plantuml
@startuml

title Manually Flip Switch
participant Io
participant TagDatabase as td

[-> Io ++ : Switch Flipped\n(InterruptHandler())
Io -> td : SetTag("Switch1", true)
return

@enduml
```

```plantuml
@startuml

title Set Switch from User Interface
participant TrackCtrlGUI as gui
participant "SWTrackCtrl::\nRequestManager" as swtcrm
participant "HWTrackCtrl::\nRequestManager" as hwtcrm
participant "connector script" as cs
participant Serial
participant Communications as comms
participant TagDatabase as td

[-> gui ++ : click
gui -> swtcrm ++ : HandleRequest(SWTRACK_SET_SWITCH)
swtcrm -> hwtcrm ++ : HandleRequest(\nHWTRACK_SET_TAG_VALUE)
hwtcrm -> hwtcrm : AddRequest(\nHWTRACK_SET_TAG_VALUE)
return
return
deactivate gui

activate cs
cs -> hwtcrm ++ : GetNextRequest()
return pRequest
cs -> Serial -- : write(request)
activate comms
comms -> Serial ++ : readline()
return message
comms -> comms ++ : SetTagValue("Switch1", true)
comms -> td : SetTag("Switch1", true)
return

@enduml
```