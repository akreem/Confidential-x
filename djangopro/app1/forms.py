from django import forms

class CreateNewSoc(forms.Form):
    uid = forms.CharField(label="المعرف الوحيد", max_length=200)
    name = forms.CharField(label="الإسم بالعربية", max_length=200)
    namefr = forms.CharField(label="الإسم بالفرنسية", max_length=200)
    res = forms.CharField(label="العنوان", max_length=200)
    tel = forms.CharField(label="رقم الهاتف", max_length=10)

class UpdateEnqextint(forms.Form):
    gharadhs = (
        ('9', '9 - مترشح قصـد متابعـة تربـص بـالمؤسسـات العسكريــة'),
        ('40', '40 - مترشح قصد آداء الواجب الوطني'),
        ('44','44 - مترشح قصـد التعامـل مـع المؤسسـات العسكريـة'),
        ('19','19 - مترشح قصد التعامل مع المؤسسات العسكرية'),
        ('18','18 - مترشح قصد متابعة تربص بالمؤسسات العسكرية'),
        ('12','12 - مترشح قصد إنتدابه للعمل بصفوف جيش البر كتلميذ ضابط صف'),
        ('13','13 - مترشح قصد إنتدابه للعمل بصفوف الجيش كتلميذ ضابط صف تقني سامي'),
        ('14','14 - مترشح قصد إنتدابه للعمل بصفوف الجيش كتلميذ رقيب'),
        ('15','15 - مترشح قصد إنتدابه للعمل بصفوف الجيش كتلميذ رقيب'),
        ('16','16 - مترشح قصد إنتدابه للعمل بصفوف جيش البحر كتلميذ ضابط صف'),
        ('17','17 - مترشح قصد إنتدابه للعمل بصفوف الجيش كتلميذ رقيب'),
        ('18','18 - مترشح قصد متابعة تربص بالمؤسسات العسكرية'),
        ('19','19 - مترشح قصد التعامل مع المؤسسات العسكرية'),
        ('20','20 - مترشح قصد الرجوع إلى صفوف الجيـش الوطني'),
        ('21','21 - مترشح قصد إدماجه بصفوف الجيش الوطني في نطاق عملية التجنيد الإستثنائية')
    )
    gharadh = forms.ChoiceField(label="رمز الغرض", choices=gharadhs)
    theyear = forms.IntegerField(label="السنة")
    tadhminfrom = forms.IntegerField(label="تضمين من")
    tadhminto = forms.IntegerField(label="تضمين إلى")
    ref = forms.CharField(label="مرجع البحث الخارجي", max_length=200)
    dateref = forms.DateField(label="تاريخ م البحث الخارجي")

class AsyncenqextForm(forms.Form):
    gender = (
        ('ذكر','ذكر'),
        ('أنثى','أنثى')
    )
    cin = forms.CharField(label="ب ت و", max_length=200)
    nom = forms.CharField(label="اللقب", max_length=200)
    prenom = forms.CharField(label="الإسم", max_length=200)
    prenpere = forms.CharField(label="اسم الاب", max_length=200)
    prengpere = forms.CharField(label="اسم الجد", max_length=200)
    nomprenmere = forms.CharField(label="اسم الام ولقبها", max_length=200)
    sex = forms.ChoiceField(label="الجنس", choices=gender)
    lieunais = forms.CharField(label="مكان الولادة", max_length=200, required=False)
    datnais = forms.CharField(label="تاريخ الولادة",  widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}), required=False)
    datecin = forms.CharField(label="تاريخ اصدار ب ت و", widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}), required=False)
    sitfam = forms.CharField(label="الحالة العائلية ", max_length=200, required=False)
    residence = forms.CharField(label="العنوان", max_length=200)
    nationalite = forms.CharField(label="الجنسية", max_length=200, initial='تونسية', required=False)
    profession = forms.CharField(label="المهنة", max_length=200, required=False)
    cod_societe = forms.CharField(label="رمز الشركة", required=False, max_length=200)
    codtype = forms.CharField(label="الغرض", max_length=200, initial='440')    

class FindCourForm(forms.Form):
    refcour = forms.CharField(label="رقم البريد", max_length=200, required=False)
    datecour = forms.CharField(label="تاريخ البريد",widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}), required=False)

class FindcivilForm(forms.Form):
    cin = forms.CharField(label="ب.ت.و", max_length=200, required=False)
    prenom = forms.CharField(label="الإسم", max_length=200, required=False)
    nom = forms.CharField(label="اللقب", max_length=200, required=False)
    prenpere = forms.CharField(label="اسم.الاب", max_length=200, required=False)
    prengpere = forms.CharField(label="اسم.الجد", max_length=200, required=False)
    nomprenmere = forms.CharField(label="اسم.الام", max_length=200, required=False)
