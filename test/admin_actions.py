import csv
import codecs
import cStringIO
from StringIO import StringIO  
from zipfile import ZipFile  
from django.http import HttpResponse
from django.db.models import Q
from test.models import (Trial, Participant, Test)                                      #Participant, Test hinzugefuegt

export_info_participant = [
    ("Testname", "test"),                                                  #hinzugefuegt
    ("Participant ID", "id"),                                                   #
    ("Identifier", "identifier"),                                               #ende hinzugefuegt
]
export_info_trial = [
    ("Date", "date"),
    ("Time", "time"),
    ("Experimental Group", "experimental_group"),
    ("Block", "block"),
    ("Practice", "practice"),
    ("Primary Left Category", "primary_left_category"),
    ("Secondary Left Category", "secondary_left_category"),
    ("Primary Right Category", "primary_right_category"),
    ("Secondary Right Category", "secondary_right_category"),
    ("Stimulus", "stimulus"),
    ("Latency", "latency"),
    ("Correct", "correct"),
]

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def export_as_csv(modeladmin, request, queryset):
#    export_info = export_info_participant + export_info_trial
    headers, fields = zip(*export_info_trial)     
#    fields_trial = zip(*export_info_trial)
    headers_participant, fields_participant = zip(*export_info_participant)
    in_memory = StringIO()  
    zipFile = ZipFile(in_memory, 'w')  
    rows = headers_participant + headers
    result_row = []
    result_row.append(rows)
    for participant in queryset:
        row1=[]
#        row2=[]
        participants = Participant.objects.filter(id=participant.id)    #alle participants mit der gleichen id werden ausgegeben
        trials = Trial.objects.filter(participant=participant.id)               #hier muss irgendwie der Participant noch mit rein
        for participant_value_list in participants.values_list(*fields_participant):
            row1.extend([unicode(v) for v in participant_value_list])
        for trial_value_list in trials.values_list(*fields):
#            row1=[]
            row2=[]
#            row1.extend([unicode(v) for v in participants.values_list(*fields_participant)])
            row2.extend([unicode(v) for v in trial_value_list])
            row = row1 + row2
#            encoded = [[s.encode('utf8') for s in t] for t in row]
            result_row.append(row)
            
#        row = rows + row1 + row2
#        result_row.append(row)
        
    f = StringIO()
    #writer = csv.writer(f)
    writer = UnicodeWriter(f)                                               
    for row in result_row:
        writer.writerow(row)

    zipFile.writestr('Results.csv', f.getvalue())  
        
    for file in zipFile.filelist:  
        file.create_system = 0      
    
    zipFile.close()
    
    response = HttpResponse(mimetype='application/zip')  
    response['Content-Disposition'] = 'attachment; filename=results.zip'
#    response = HttpResponse(mimetype='text/csv')  
#    response['Content-Disposition'] = 'attachment; filename=result.csv'
    
    in_memory.seek(0)      
    response.write(in_memory.read())
    
    return response    

export_as_csv.short_description = "Export as CSV"
