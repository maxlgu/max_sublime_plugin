import sublime
import sublime_plugin
import re
import urllib

# view.run_command('suggest_import')
class SuggestImport(sublime_plugin.TextCommand):
  def run(self, edit):
    class_names = self.find_import_class_names();
    print('Found {} imports:{}'.format(len(class_names), [s for s in class_names]))
    import_world_text = self.get_import_world_text();
    for class_name in class_names:
      match = re.search("import\s.*\.{};".format(class_name), import_world_text)
      if match:
        line = match.group(0)
        print("found: "+line)
        self.view.insert(edit, self.view.size(), "\n"+line )
    # self.view.insert(edit, self.view.size(), "\n====== End ========")

  def get_import_world_text(self):
    with open("/usr/local/google/home/maxlg/.config/sublime-text-3/Packages/User/all_imports.txt","r") as file:
      all_imports = file.read()
    return all_imports

  def find_import_class_names(self):
    results = []
    # symbol: class OnGlobalLayoutListener
    regions = self.view.find_all('symbol:\s+class\s\w+')
    print("Found {} regions".format(len(regions)))
    for region in regions:
      symbol_line = self.view.substr(region)
      print("symbol_line: "+symbol_line)
      query = re.search('symbol:\s+class\s(\w+)', symbol_line)
      if query:
        class_name = query.group(1)
        results.append(class_name)
    return results
