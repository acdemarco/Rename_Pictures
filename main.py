# This is a sample Python script.
import Rename_All as RA
import PySimpleGUI as sg

label = sg.Text("Source Folder: ")
label2 = sg.Text("Rename Number: ")
label3 = sg.Text("Target extension (jpeg,gif, etc.): ")
label4 = sg.Text("Destination Folder: ")

Input_Source = sg.InputText(tooltip="Enter Source Folder.", key='Source_Folder')
Input_Destf = sg.InputText(tooltip="Enter Destination Folder.", key='Dest_Folder')
Input_Dest = sg.InputText(tooltip="Enter Starting number for rename.", key='Rename_number')
Input_Ext = sg.InputText(tooltip="Enter Target Ext.", key='Source_Ext')
choose_folder = sg.FolderBrowse("Folder...")
choose_folder2 = sg.FolderBrowse("Folder...")

run_button = sg.Button("Run")
exit_button = sg.Button("Exit")

window = sg.Window("Rename Image Files",
                   layout=[
                       [label, Input_Source, choose_folder],
                       [label4,Input_Destf, choose_folder2],
                       [label2], [Input_Dest], [label3], [Input_Ext],
                       [exit_button, run_button]
                        ], font=('Helvetica', 20))
while True:
    event, value = window.read()
    print(event)
    print(value)
    match event:
        case "Run":
            print("Run")
            SourceFolder = value['Source_Folder']
            DestFolder = value['Dest_Folder']
            StartNum = int(value['Rename_number'])
            DestExt = value['Source_Ext']
            print(SourceFolder, DestFolder,StartNum, DestExt)
            RA.walktree(SourceFolder, DestExt, StartNum, DestFolder ,RA.visitfile)
            sg.popup("Program Done", "The program has completed its task.")
            break
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
