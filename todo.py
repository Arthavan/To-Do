#Based on the Tutorial by Flet Docs
#Modified by Arthavan.

from time import sleep
import flet as ft


class Task(ft.UserControl):

  def __init__(self, task_name, task_delete):
    super().__init__()
    self.task_name = task_name
    self.task_delete = task_delete

  def build(self):
    self.display_task = ft.Checkbox(value=False, label=self.task_name)
    self.edit_name = ft.TextField(expand=1, on_submit=self.save_clicked)

    self.display_view = ft.Row(
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.display_task,
        ft.Row(
          spacing=0,
          controls=[
            ft.IconButton(
              icon=ft.icons.CREATE_OUTLINED,
              tooltip="Edit To-Do",
              on_click=self.edit_clicked,
            ),
            ft.IconButton(
              ft.icons.DELETE_OUTLINE,
              tooltip="Delete To-Do",
              on_click=self.delete_clicked,
            ),
          ],
        ),
      ],
    )

    self.edit_view = ft.Row(
      visible=False,
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.edit_name,
        ft.IconButton(
          icon=ft.icons.DONE_OUTLINE_OUTLINED,
          icon_color=ft.colors.GREEN,
          tooltip="Update To-Do",
          on_click=self.save_clicked,
        ),
      ],
    )
    return ft.Column(controls=[self.display_view, self.edit_view])

  def edit_clicked(self, e):
    self.edit_name.value = self.display_task.label
    self.display_view.visible = False
    self.edit_view.visible = True
    self.update()

  def save_clicked(self, e):
    self.display_task.label = self.edit_name.value
    self.display_view.visible = True
    self.edit_view.visible = False
    self.update()

  def delete_clicked(self, e):
    self.task_delete(self)

  def enlarge(self, e):
    self.edit_name.text_style = ft.TextThemeStyle.BODY_LARGE


class TodoApp(ft.UserControl):

  def __init__(self, page):
    super().__init__()
    self.page = page
    self.task_list = []
    self.tasks = ft.Column()
    

  def build(self):
    self.new_task = ft.TextField(
      hint_text="Write a task and then either press the + button or hit enter!",
      expand=True,
      on_submit=self.add_clicked)
    self.tasks = ft.Column()

    #FUNCTIONS

    #Dark/Light mode
    settings_button = ft.IconButton(icon=ft.icons.SETTINGS)
    settings_button.visible = False
    file_button = ft.IconButton(icon=ft.icons.FOLDER,
                                on_click=self.load,
                                tooltip="Load Saved Tasks")
    save_button = ft.IconButton(icon=ft.icons.SAVE_AS,
                                on_click=self.save,
                                tooltip="Save Current Tasks")
    clear_button = ft.IconButton(icon=ft.icons.CANCEL,
                                 on_click=self.clear,
                                 tooltip="Clear Saved Tasks")
    light_button = ft.IconButton(icon=ft.icons.LIGHT_MODE,
                                 on_click=self.change_theme_light,
                                 tooltip="Click for Light Theme")
    dark_button = ft.IconButton(icon=ft.icons.DARK_MODE,
                                on_click=self.change_theme_dark,
                                tooltip="Click for Dark Theme")
    line_button = ft.TextButton(text="", disabled=True)
    #scale_up_button = ft.IconButton(icon=ft.icons.EXPAND_LESS)
    #abc_button = ft.IconButton(icon=ft.icons.ABC, disabled=True)
    #scale_down_button = ft.IconButton(icon=ft.icons.EXPAND_MORE)

    return ft.Column(controls=[
      ft.Row(controls=[
        ft.FloatingActionButton(icon=ft.icons.ADD,
                                on_click=self.add_clicked,
                                tooltip="Click to Add Task"), self.new_task
      ]),
      ft.Row([
        settings_button, file_button, save_button, clear_button, line_button,
        light_button, dark_button
      ],
             alignment=ft.MainAxisAlignment.CENTER), self.tasks
    ])

  def task_delete(self, task):
    self.tasks.controls.remove(task)
    self.update()

  def add_clicked(self, e):
    if self.new_task.value != "":
      task = Task(self.new_task.value, self.task_delete)
      self.tasks.controls.append(task)
      self.task_list.append(self.new_task.value)
      self.new_task.value = ""
      self.update()

  #Dark/Light theme
  def change_theme_dark(self, e):
    self.page.theme_mode = ft.ThemeMode.DARK
    self.page.update()

  def change_theme_light(self, e):
    self.page.theme_mode = ft.ThemeMode.LIGHT
    self.page.update()

  def ld(self):
    if self.page.client_storage.__sizeof__() > 1:
      for t in self.page.client_storage.get("stuff"):
        self.task_list.append(t)
        self.tasks.controls.append(Task(t, self.task_delete))
        self.update()
        sleep(0.4)

  def sv(self):
    self.page.client_storage.set("stuff", self.task_list)

  def load(self, e):
    for t in self.page.client_storage.get("stuff"):
      self.tasks.controls.append(Task(t, self.task_delete))
      self.task_list.append(t)
      self.update()
      sleep(0.1)

  def save(self, e):
    self.page.client_storage.set("stuff", self.task_list)

  def clear(self, e):
    self.page.client_storage.set("stuff", [])


def main(page: ft.Page):
  #Initialization
  page.title = "To-Do Application"
  page.horizontal_alignment = ft.CrossAxisAlignment.START
  page.update()
  page.theme_mode = ft.ThemeMode.SYSTEM
  todo = TodoApp(page)
  page.add(todo)
  todo.ld()


ft.app(target=main)
