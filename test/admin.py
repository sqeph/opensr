from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from test.admin_actions import export_as_csv
from test.models import (Test, Block, ExperimentalGroup, Trial, Stimulus, Category, Participant, StimuliOrder)
from test.forms import (AtLeastOneFormSet, PageForm)
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.sites.models import Site

class StimulusInline(admin.TabularInline):
    model = Stimulus 
    #fields = ('word', 'image','id')
    #readonly_fields = ['id']
    verbose_name_plural='Stimulus'
    extra = 1
    formset = AtLeastOneFormSet
    
class ExperimentalGroupInline(admin.StackedInline):
    model = ExperimentalGroup
    extra = 1
    formset = AtLeastOneFormSet
    
class TrialInline(admin.TabularInline):
    model = Trial
    extra = 1   
    readonly_fields = ('date', 'time', 'participant', 'block', 'practice', 
                  'primary_left_category', 'secondary_left_category', 'primary_right_category', 
                  'secondary_right_category', 'stimulus', 'correct', 'latency')
    exclude = ('test', 'experimental_group', )
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
        
class TestForm(forms.ModelForm):
    
    class Meta:
        model = Test

class CategoryAdmin(admin.ModelAdmin):
    form = TestForm
    ordering = ('category_name',)
    list_display = ('category_name',)
    inlines = [
        StimulusInline
    ]
    
    def get_formset(self, request, obj=None, **kwargs):
        StimulusInline.obj = obj
        return super(CategoryAdmin, self).get_formset(request, obj, **kwargs)
    
class TestAdmin(admin.ModelAdmin):  
    form = TestForm
    ordering = ('test_name',)
    list_display = ('test_name', 'is_active')
    inlines = [
        ExperimentalGroupInline
    ]    
    
class BlockAdmin(admin.ModelAdmin):
    ordering = ('block_name',)
    search_fields = ('test__test_name', )
    list_filter = ('test__test_name', )
    list_display = ('block_name', 'test')

class PageAdmin(FlatPageAdmin):
    form = PageForm
    
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["initial"] = [Site.objects.get_current()]
        return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ParticipantAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
    ordering = ('id',)
    fields = ('test', 'experimental_group')
    list_display = ('id', 'experimental_group', 'test', 'has_completed_test', 'identifier')
    search_fields = ('experimental_group__group_name', 'test__test_name')
    readonly_fields = ('experimental_group', 'test')
    list_filter = ('experimental_group', 'test__test_name', 'test__is_active', 'has_completed_test', 'identifier')
    inlines = [
        TrialInline
    ]    
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(ParticipantAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
        
class StimuliOrderAdmin(admin.ModelAdmin):
    model=StimuliOrder
    exclude = ('block',)
    
    def has_delete_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return False
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(StimuliOrder, StimuliOrderAdmin)
admin.site.unregister(Site)
