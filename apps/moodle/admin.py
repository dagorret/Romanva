"""
Admin interface para los modelos de Moodle
"""
from django.contrib import admin
from .models import (
    Category, Course, MoodleUser, Group, GroupMember,
    Enrol, UserEnrolment, UserLastAccess, Role, RoleAssignment
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'depth', 'path']
    list_filter = ['depth']
    search_fields = ['name', 'path']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['shortname', 'fullname', 'category', 'startdate', 'visible']
    list_filter = ['category', 'visible', 'startdate']
    search_fields = ['shortname', 'fullname']
    date_hierarchy = 'startdate'


@admin.register(MoodleUser)
class MoodleUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'lastname', 'firstname', 'email']
    search_fields = ['username', 'firstname', 'lastname', 'email']
    ordering = ['lastname', 'firstname']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'course']
    list_filter = ['course']
    search_fields = ['name', 'course__shortname', 'course__fullname']


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'timeadded']
    list_filter = ['group__course', 'timeadded']
    search_fields = ['user__username', 'user__lastname', 'group__name']
    date_hierarchy = 'timeadded'


@admin.register(Enrol)
class EnrolAdmin(admin.ModelAdmin):
    list_display = ['course', 'enrol', 'status']
    list_filter = ['enrol', 'status']
    search_fields = ['course__shortname', 'course__fullname']


@admin.register(UserEnrolment)
class UserEnrolmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrol', 'timestart', 'timeend']
    list_filter = ['enrol__course', 'timestart']
    search_fields = ['user__username', 'user__lastname', 'enrol__course__shortname']
    date_hierarchy = 'timecreated'


@admin.register(UserLastAccess)
class UserLastAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'timeaccess']
    list_filter = ['course', 'timeaccess']
    search_fields = ['user__username', 'user__lastname', 'course__shortname']
    date_hierarchy = 'timeaccess'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortname']
    list_filter = ['shortname']
    search_fields = ['name']


@admin.register(RoleAssignment)
class RoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'course', 'timecreated']
    list_filter = ['role', 'course', 'timecreated']
    search_fields = ['user__username', 'user__lastname', 'role__name', 'course__shortname']
    date_hierarchy = 'timecreated'
