class Pagination:
  def __init__(self, objects):
    self.objects = objects
  
  def pagination(self):
    pages = []
    page = []
    count = 0
    page_position = 0

    for object in self.objects:
      
      if count <= 5:
        page.append(object)
      
      if count == 0 :
        pages.append(page)

      if count == 5:
        page = []
        count = 0
        page_position += 1
      else:
        count += 1

    return pages