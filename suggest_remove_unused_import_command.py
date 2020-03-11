import sublime
import sublime_plugin
import re

# view.run_command('suggest_remove_unused_import')
class SuggestRemoveUnusedImportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    class_names = self.find_import_class_names();
    print('Found {} imports'.format(len(class_names)))
    whole_text = self.get_whole_text();
    for class_name in class_names:
      matches = re.findall("[^\w]{}[^\w]".format(class_name), whole_text)
      if len(matches) <= 1:
        print('Marked: '+class_name)
        # self.comment(edit, self.find_region_by_name(class_name), 'TODO(maxlg@): remove unused import')
        self.delete(edit, self.find_region_by_name(class_name))

  def comment(self, edit, region, text):
    new_string = self.view.substr(region) + "  // " +text
    self.view.replace(edit, region, new_string)

  def delete(self, edit, region):
    new_string = ""
    self.view.replace(edit, region, new_string)

  def find_region_by_name(self, class_name):
    return self.view.find('^import.*\.{};$'.format(class_name), 0)

  def get_whole_text(self):
    return self.view.substr(sublime.Region(0, self.view.size()))
  def find_import_class_names(self):
    results = []
    for region in self.view.find_all('^import.*;$'):
      import_line = self.view.substr(region)
      query = re.search('import.*\.(\w+);', import_line)
      if query:
          class_name = query.group(1)
      results.append(class_name)
    return results

