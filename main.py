# This is a sample Python script.
import Rename_All as RA
import PySimpleGUI as sg

label = sg.Text("Enter Source Folder: ")
label2 = sg.Text("Enter Destination Folder: ")
label3 = sg.Text("Enter target extension (mp3, etc.): ")

Input_Source = sg.InputText(tooltip="Enter Source Folder.", key='Source_Folder')
Input_Dest = sg.InputText(tooltip="Enter Destination Folder.", key='Dest_Folder')
Input_Ext = sg.InputText(tooltip="Enter Target Ext.", key='Source_Ext')

run_button = sg.Button("Run")
exit_button = sg.Button("Exit")

window = sg.Window("Rename Music Files",
                   layout=[[label], [Input_Source], [label2],
                         [Input_Dest], [label3], [Input_Ext],
                         [exit_button, run_button]],
                   font=('Helvetica', 20))
while True:
    event, value = window.read()
    print(event)
    print(value)
    match event:
        case "Run":
            print("Run")
            SourceFolder = value['Source_Folder']
            DestFolder = value['Dest_Folder']
            DestExt = value['Source_Ext']
            print(SourceFolder,DestFolder,DestExt)
            RA.walktree(SourceFolder, DestExt, RA.visitfile)
        case "Exit":
            # exit(0)
            break
        case sg.WINDOW_CLOSED:
            # exit(0)
            break


window.close()


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
