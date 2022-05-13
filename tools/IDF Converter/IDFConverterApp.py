"""
Classes for the IDF Converter's GUI
The script uses mostly the same functions as the IDF_converter.py but they are tailored to guide user throughout the process
This script requires a kv file which holds most of the layout properties
Kivy uses both py and kv files bidirectionally, even kv file has a lot functions embedded to individual gadgets.
Copyright: Sahin AKIN, 2022
"""

#ScreenResolution Settings
from kivy.config import Config
Config.set('graphics','resizable',0)
Config.set("graphics","fullscreen","0")
from kivy.core.window import Window
Window.borderless = False

#Importing required packages
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import kivy
kivy.require('1.0.8')

#Importing main converter script
from IDF_converter import *

#Each class corresponds whether to a widget or a screen
class Welcome(Screen):
    """
    Welcome Screen: includes information section about BuildME
    """
    pass

class Finish(Screen):
    """
    Final Screen: includes final summary, next stages and caution sections
    """
    layoutf = ObjectProperty(None)
    pass


class MyWidget(BoxLayout):
    """
    Project Browser gadget for IDF file selection
    User can select an item by clicking the Load button
    The script gets the file path and puts into a list

    def selected: gets the file path once the file is selected on Filechooser
    def save: appends the file path to a list
    """
    idfpath= ObjectProperty(None)
    idfpathlist = []

    def selected(self, filename):
        self.idfpath.text = f"{filename[0]}"

    def save(self,  idfpathlist, path, filename,*args):
        global selected_idf_list
        idfpathlist.append(os.path.join(path, filename[0]))
        self.idfpath.text=str(idfpathlist)
        selected_idf_list=idfpathlist
        return
    pass


class MyWidgetsavefolder(BoxLayout):
    """
    Project Browser gadget for save folder selection
    User can select an item by clicking the Load button
    The script gets the save folder path and saves it as a variable

    def selected: gets the folder path once the file is selected on Filechooser
    def savefolder: creates a variable corresponding to the folder path
    """
    savefolderpath= ObjectProperty(None)

    def selected(self, filename):
        self.savefolderpath.text = f"{filename[0]}"

    def savefolder(self,  path, filename,*args):
        global selected_savefolder
        selected_savefolder = (os.path.join(path, filename[0]))
        self.savefolderpath.text=str(selected_savefolder)
        return
    pass


class Screen1(Screen):
    """
    Screen1: includes 2 checkboxes and a slider

    *checkboxes: checks if user complies with the requirements
    *slider: controls the IDF files to be converted

    def allowing1: Checks if the first checkbox in the screen is ticked, without this action user cannot proceed to the next phases
    def allowing2: Checks if the second checkbox in the screen is ticked, without this action user cannot proceed to the next phases
    def update_button_labels: Based on the slider value located in this screen, it creates:
        -File selection buttons in Screen 3 along with their popups
        -Text Inputs in Screen 4 for replacer strings for each IDF file
        -Folder selection button in Screen 5 along with a popup
    def updatetext: embeds the text inputs located in Screen 4 to themselves to make them accessible later
    """
    checks = []
    global allow
    global allow2
    allow=False
    allow2 = False

    def allowing1(self, instance, value):
        global allow
        if value == True:
            allow=True
        else:
            allow=False

    def allowing2(self, instance, value):
        global allow2
        if value == True:
            allow2=True
        else:
            allow2=False
    slider = ObjectProperty(None)

    #slider function controlling most of the widgets
    def update_buttons_labels(self, *args):
        global root2
        global popup2
        global textinput_replace
        global textinput_replacer
        global allow
        global allow2

        #checks if the checkboxes whether ticked
        if allow==True and allow2==True:

            #getting layouts from different screens
            layout = self.manager.get_screen('screen3').layout
            layout.clear_widgets()
            layout4 = self.manager.get_screen('screen4').layout4
            layout4.clear_widgets()
            layout5 = self.manager.get_screen('screen5').layout5
            layout5.clear_widgets()

            #gets the text input values from Screen 4
            def updatetext(kivyitem):
                kivyitem.text = kivyitem.text

            #based on the slider value for the number of IDF files to be converted, relevant buttons/text inputs/filebrowsers are created in this stage
            for i in range(int(self.slider.value)):
                if i==0:
                    #one time only events are located in this if clause

                    #creates popup file browser for save folder selection
                    root2 = MyWidgetsavefolder()
                    popup2 = Popup(content=root2, auto_dismiss=False)
                    cancelbtn = Button(text="Close", font_name="trebuc", background_color="##b56767", color=(1, 1, 1, 1),
                                       size_hint=(1, 0.10), on_press=popup2.dismiss)
                    root2.add_widget(cancelbtn)
                    layout5.add_widget(
                        ToggleButton(text="Select Save Folder", font_name="trebuc", background_color="##00838F",
                                     background_normal="##00838F",size_hint=(1, 0.2), on_release=lambda x: popup2.open()))
                    layout5.add_widget(Label(size_hint=(0.1,0.1)))
                    #creates popup file browser for IDF file selection
                    root = MyWidget()
                    popup = Popup(content=root, auto_dismiss=False)
                    cancelbtnn=Button(text="Close", font_name="trebuc", background_color="##b56767", color=(1, 1, 1, 1),size_hint=(1, 0.10),on_press=popup.dismiss)
                    root.add_widget(cancelbtnn)
                    layout.add_widget(Label(text="Phase Three",font_size=50,font_name="trebuc"))
                    layout.add_widget(Label(text=f"Select base IDF",font_name="trebuc"))
                    layout.add_widget(ToggleButton(text="Open File Browser",font_name="trebuc",background_color="##00838F",background_normal="##00838F",on_release=lambda x:popup.open()))
                    #creates replacer textinput boxes for the base IDF and replaceme rule that is effective for all IDF files on Screen 4
                    layout4.add_widget(Label(text="Phase Four", font_size=50,size_hint=( 1, 0.9), font_name="trebuc"))
                    layout4.add_widget(Label(text='[font=trebuc][color=#ffffff][b][size=13]Please specify a generic REPLACEME string about to be applied to your IDFs:[/size][/b]\n [size=11](i.e.,-en-std-replaceme-res-replaceme) [/size]',halign= 'center',markup=True))
                    textinput_replace=TextInput(size_hint_x=0.7, text="wow",size_hint_y=0.7, font_size=12, pos_hint={"x": 0.15}, height='32dp',width="100dp", multiline=False, hint_text='i.e.,-en-std-replaceme',)
                    textinput_replace.bind(on_text=lambda x:updatetext(textinput_replace))
                    layout4.add_widget(textinput_replace)
                    layout4.add_widget(Label(text=f"[size=13]Specify the replacer string for IDFs[/size]\n [size=11](i.e.,-ZEB-RES0) [/size]",markup=True,halign= 'center',font_name="trebuc"))
                    textinput_replacer=TextInput(size_hint_x= 0.7,size_hint_y= 0.7,font_size=12,pos_hint= {"x":0.15},height= '32dp',width="100dp",multiline= False,hint_text= "Specify the replacer string for the base IDF")
                    layout4.add_widget(textinput_replacer)
                    textinput_replacer.bind(on_text=lambda x: updatetext(textinput_replacer))

                else:
                    #based on the alternative IDF numbers selected, several input gadgets are created
                    #creates replacer textinput boxes for the alternative IDFs
                    root = MyWidget()
                    popup = Popup(content=root, auto_dismiss=False)
                    cancelbtnn=Button(text="Close", font_name="trebuc", background_color="##b56767", color=(1, 1, 1, 1),size_hint=(1, 0.10),on_press=popup.dismiss)
                    root.add_widget(cancelbtnn)
                    layout.add_widget(Label(text=f"Select alternative IDF {i}",font_name="trebuc"))
                    layout.add_widget(ToggleButton(text=f"Open File Browser for IDF {i}",font_name="trebuc",background_color="##00838F",background_normal="##00838F",on_release=lambda x:popup.open()))
                    globals()['textinput_replacer%s' % i]=TextInput(size_hint_x= 0.7,size_hint_y= 0.7,font_size=11,pos_hint= {"x":0.15},height= '32dp',width="100dp",multiline= False,hint_text= f"Specify the replacer string for the alternative IDF {i}")
                    layout4.add_widget(globals()['textinput_replacer%s' % i])
                    globals()['textinput_replacer%s' % i].bind(on_text=lambda x:updatetext(globals()['textinput_replacer%s' % i]))
    pass



class Screen2(Screen):
    """
    Screen2: includes 2 textinput files

    *textinputs: defines Region and Occupation fields

    def process_input1: returns the user input for Region
    def process_input2: returns the user input for Occupation
    """
    #Region
    def process_input1(self):
        global returntextinput1
        returntextinput1 = self.ids.textinput1.text
        return returntextinput1
    #Occupation
    def process_input2(self):
        global returntextinput2
        returntextinput2 = self.ids.textinput2.text
        return returntextinput2
    pass


class Screen3(Screen):
    """
    Screen3: includes file browsers for IDF selection, controlled by the slider value located at Screen 1

    *filebrowsers: gets the individual paths for IDF files to be converted, the first one should be the base IDF
    """
    layout = ObjectProperty(None)
    pass


class MyScreenManager(ScreenManager):
    """
    ScreenManager: controls all screens and their transitions

    def changescreen: function to change the current screen to another
    """
    def changescreen(self, value):
        self.transition = FadeTransition()
        self.current = value




class Screen4(Screen):
    """
    Screen4: includes 1 information label, 2 types of texinputs

    *information label: shows the selected IDFs, the first one should be the base idf
    *textinput type 1: defines the replaceme string content. For now BuildME can support "-en-std-replaceme" and "-res-replaceme"
    but user can define new layers as well such as cohorts or climate characteristics. In that case, user should make sure that each
    inserted replacement layer should contain "replaceme" afterwards.Also, the main BuildME script should be edited
    to accommodate the new layers.  For instance it is also possible to input "-en-std-replaceme-res-replaceme-chrt-replaceme".

    *textinput type 2: defines the replacer string for each IDF files. If the particular IDF file has values corresponding to an efficient version,
    user needs to input "-efficient" to the field. An IDF file can also inherit different layer characteristics as well. For instance it is also possible
    to input -efficient-RES0-1920.

    def update_IDF_label: returns the selected files as a dictionary and visualizes as an information label
    """
    layout4 = ObjectProperty(None)
    idfs= ObjectProperty(None)
    #creates the information label
    def update_IDF_label(self, *args):
        slider = self.manager.get_screen('screen1').layout1
        mylabel = self.manager.get_screen('screen4').idfs
        selectedidflist_keys = []
        selectedidflist_values = []
        if int(float(slider.text)) > 0:
            for i in range(int(float(slider.text))):
                if i==0:
                    selectedidflist_keys.append(F"Base IDF")
                else:
                    selectedidflist_keys.append(F"IDF{i}")
            for i in selected_idf_list:
                print(type(selected_idf_list))
                selectedidflist_values.append(i)
            mydict = dict(zip(selectedidflist_keys, selectedidflist_values))
            mystring=str(mydict)
            #dictionary converted to a multiline string
            while "," in mystring:
                mystring=mystring.replace(",","\n")
                mystring = mystring.replace("{", "")
                mystring = mystring.replace("}", "")
                mylabel.text = f"[b]The selected IDFs are:[/b] \n[size=14]{mystring}[/size]"
        else:
            mylabel.text = "Please go back and select some IDF files and tick the checkboxes!"
    pass


class Screen5(Screen):
    """
    Screen5: includes 1 checkbox, 1 filebrowser

    *checkbox: gives an option to create a non-standard version of the base IDF. User needs to make sure that base IDF has a replacer value defined including "standard" string in it.
    *filebrowser: prompts user to select a save folder for output files

    def checkbox_click: returns a boolean value to be used in creating the non-standard version of the base IDF file
    def convert: converts each of the idf files and saves them separately to the savefolder
    """

    global nonstandard
    nonstandard=True

    def checkbox_click(self, instance, value):
        if value == True:
            print("non-standard version will be created")
            nonstandard=True
        if value==False:
            print("non-standard version will not be included")
            nonstandard = False

    def convert(self, *args):
        global textinput_replacer
        global textinput_replace

        counter=0
        if nonstandard==True:
            for i in selected_idf_list:
                if counter==0:
                    convert_idf_to_BuildME(i, selected_savefolder, replace_string=textinput_replace.text,replace_string_value=textinput_replacer.text, base=True)
                    #creates the non-standard version
                    if "standard" in textinput_replacer.text:
                            nons="{}".format("-non"+textinput_replacer.text)
                            print(nons)
                            counter = counter + 1
                            convert_idf_to_BuildME(i, selected_savefolder, replace_string=textinput_replace.text,
                                                   replace_string_value=nons, base=False)
                    else:
                        raise Exception(" selected replacer value for the base IDF does not corresponding to an energy standard. The replacer input should contain standard")
                        app.close()
                else:
                    textinput_replacer = globals()['textinput_replacer%s' % counter]
                    counter = counter + 1
                    convert_idf_to_BuildME(i, selected_savefolder, replace_string=textinput_replace.text,
                                           replace_string_value=textinput_replacer.text,base=False)
        #if the checkbox is unticked for non-standard version, the script skips this stage
        if nonstandard == False:
            for i in selected_idf_list:
                if counter == 0:
                    counter = counter + 1
                    convert_idf_to_BuildME(i, selected_savefolder, replace_string=textinput_replace.text,
                                           replace_string_value=textinput_replacer.text, base=True)
                else:
                    textinput_replacer = globals()['textinput_replacer%s' % counter]
                    counter = counter + 1
                    convert_idf_to_BuildME(i, selected_savefolder, replace_string=textinput_replace.text,
                                           replace_string_value=textinput_replacer.text, base=False)
    pass


class Screen6(Screen):
    """
    Screen6: includes 1 checkbox for merge option, 2 checkboxes for output filetype selection

    *checkbox: gives an option to create a non-standard version of the base IDF. User needs to make sure that base IDF has a replacer value defined including "standard" string in it.
    *filebrowser: prompts user to select a save folder for output files

    def checkbox_clickmerge: returns a boolean value to be used in creating the non-standard version of the base IDF file
    def checkbox_yaml: returns a boolean value to be used in creating the outputs in yaml format
    def checkbox_xlsx: returns a boolean value to be used in creating the outputs in xlsx format
    def finalshot: based on the boolean values, creates all output files and merged idf file that is compatible with BuildME and creates the final summary content that is displayed in Finish screen
    """
    xlsx = ObjectProperty(None)
    yaml = ObjectProperty(None)

    global merged
    merged = True
    #cheking if the merge option is selected, if not program is terminated with only individual converted items
    def checkbox_clickmerge(self, instance, value):
        if value == True:
            merged=True
            print("All IDF combinations will be merged")
        if value==False:
            merged = False
            print("Individual output files will not be produced, you will need to merge them by yourself in order to simulate combinations via BuildME")

    global yamlcreator
    global xlsxcreator
    yamlcreator = False
    xlsxcreator = False
    #checks the yaml checkbox
    def checkbox_yaml(self, instance, value):
        global yamlcreator
        global xlsxcreator
        if value==True:
            yamlcreator=True
            print("yaml files will be created")
        if value==False:
            yamlcreator=False
            print("yaml files will not be included")

    # checks the xlsx checkbox
    def checkbox_xlsx(self, instance, value):
        global yamlcreator
        global xlsxcreator
        if value==True:
            xlsxcreator=True
            print("XLSX files will be created")
        if value==False:
            xlsxcreator=False
            print("XLSX files will not be included")
    #Magic!
    def finalshot(self):
        global yamlcreator
        global xlsxcreator
        global returntextinput1
        global returntextinput2
        listed = create_combined_idflist(selected_savefolder)
        if merged==True:
            mergedidf = create_combined_idf_archetype(selected_savefolder, listed)
        if yamlcreator == True:
            summarytext, nextstepstext, cautiontext, Region, Occupation=update_all_datafile_yaml_gui(listed, mergedidf, selected_savefolder, Region=returntextinput1, Occupation=returntextinput2)
        if xlsxcreator == True:
            summarytext, nextstepstext, cautiontext, Region, Occupation=update_all_datafile_xlsx_gui(listed, mergedidf,selected_savefolder, Region=returntextinput1, Occupation=returntextinput2)
        breakdown = self.manager.get_screen('finish').layoutf
        breakdown.text=f'[font=trebuc][color=#ffffff][b][size=30]BuildME[/size][/b]\n[size=16]Framework to calculate building material & energy expenditures.[/size]\n[/color][/font][font=trebuc][size=14][color=#93c47d]\n[b]SUMMARY:[/b][/size]\n[size=12]{summarytext}, {Region}, {Occupation}\n\n[color=#ffe599][b]NEXT STEPS:[/b]\n{nextstepstext}\n[color=#ea9999][b]CAUTION:[/b]\n{cautiontext}\n[/color][/size][/font]\n[font=trebuc][size=10][color=#d0e0e3][b]Authors & contributions[/b]\n[i]Niko Heeren, Andrea Nistad, Kamila Krych, Sahin Akin[/i]\nCopyright:[i]Niko Heeren[/i], 2021[/color][/size][color=#000000][/color][/font]'
    pass

class converterApp(App):
    """
    converterApp: This is the main application for the GUI that is the compilation of everything
    """

    def build(self):
        self.title = 'IDF Converter for BuildME'
        self.sm = MyScreenManager(transition = FadeTransition())
        self.title = 'IDF Converter for BuildME'
        return self.sm

if __name__ == '__main__':
    converterApp().run()
