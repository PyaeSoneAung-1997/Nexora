from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar
class menubar(QMenuBar):
        def __init__(self,main_window):
                super().__init__(main_window)
                self.main_window = main_window
                self.setup()                

        def setup(self):
                
                #Tasks
                task_menu = self.addMenu("Tasks")
                self.add_new_download_action = task_menu.addAction("Add New Download")
                self.add_batch_download_action = task_menu.addAction("Add Batch Download")
                self.add_batch_clipboard_action = task_menu.addAction("Add Batch Download From Clipboard")
                self.run_site_grabber_action = task_menu.addAction("Run Site Grabber")
                task_menu.addSeparator()
                self.show_drop_target_action = task_menu.addAction("Show Drop Target")
                task_menu.addSeparator()
                self.export_action = task_menu.addAction("Export")
                self.import_action = task_menu.addAction("Import")
                task_menu.addSeparator()
                self.exit_action = task_menu.addAction("Exit")

                #File
                file_menu = self.addMenu("File")
                self.stop_download_action = file_menu.addAction("Stop Download")
                self.remove_download_action = file_menu.addAction("Remove Download")
                self.download_now_action = file_menu.addAction("Download Now")

                #Downloads
                downloads_menu = self.addMenu("Downloads")
                self.pause_all_action = downloads_menu.addAction("Pause All")
                self.stop_all_action = downloads_menu.addAction("Stop All")
                downloads_menu.addSeparator()
                self.delete_all_complete_action = downloads_menu.addAction("Delete All Complete")
                downloads_menu.addSeparator()
                self.find_action = downloads_menu.addAction("Find")
                self.find_next_action = downloads_menu.addAction("Find Next")
                self.find_previous_action = downloads_menu.addAction("Find Previous")
                downloads_menu.addSeparator()
                self.schedule_action = downloads_menu.addAction("Schedule")
                self.start_queue_action = downloads_menu.addAction("Start Queue")
                self.stop_queue_action = downloads_menu.addAction("Stop Queue")
                downloads_menu.addSeparator()
                self.speed_limiter_action = downloads_menu.addAction("Speed Limiter")
                downloads_menu.addSeparator()
                self.options_action = downloads_menu.addAction("Options")


                #View
                view_menu = self.addMenu("View")
                self.show_categories_action = view_menu.addAction("Show Categories")
                self.arrange_files_action = view_menu.addAction("Arrange Files")
                self.show_toolbar_action = view_menu.addAction("Toolbar")
                self.nexora_tray_icon_action = view_menu.addAction("Nexora Tray Icon")
                self.customize_url_list_action = view_menu.addAction("Customize URL List")
                self.dark_mode_support_action = view_menu.addAction("Dark Mode Support")
                self.font_action = view_menu.addAction("Font")
                view_menu.addSeparator()
                self.language_action = view_menu.addAction("Language")

                #Help
                help_menu = self.addMenu("Help")               
                self.help_contents_action = help_menu.addAction("Help Contents")
                self.tutorials_action = help_menu.addAction("Tutorials")
                self.scheduler_and_queues_action = help_menu.addAction("Scheduler and Queues")
                self.grabber_help_action = help_menu.addAction("Grabber Help")
                self.tip_of_the_day_action = help_menu.addAction("Tip of the Day")
                help_menu.addSeparator()
                self.nexora_home_page_action = help_menu.addAction("Nexora Home Page")
                self.contact_nexora_support_action = help_menu.addAction("Contact Nexora Support")
                help_menu.addSeparator()
                self.check_for_updates_action = help_menu.addAction("Check for Updates")
                help_menu.addSeparator()
                self.about_nexora_action = help_menu.addAction("About Nexora")
                self.tell_a_friend_action = help_menu.addAction("Tell a Friend")

                #Registration
                registration_menu = self.addMenu("Registration")
                #order online,registration
                self.order_online_action = registration_menu.addAction("Order Online")
                self.registration_action = registration_menu.addAction("Registration")



                # self.new_action.triggered.connect(
                #         self.main_window.new_file
                # )
                # file_menu.addAction(
                #         self.new_action
                # )



                
                

                # # Edit
                # edit_menu = menu_bar.addMenu("Edit")

                # edit_menu.addAction("Undo")
                # edit_menu.addAction("Redo")

                # # View
                # view_menu = menu_bar.addMenu("View")

                # view_menu.addAction("Sidebar")
                # view_menu.addAction("Toolbar")

                
                
                # self.about_action = help_menu.addAction("About")

