from django.contrib import admin
from django.contrib.auth.models import Group
from .metrics import metrics

# 先取消注册内置的 GroupAdmin
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """自定义 Group 管理后台，添加 StatsD 指标上报"""
    
    @metrics.admin_metrics('auth.group.add')
    def add_view(self, request, form_url='', extra_context=None):
        """添加组的视图，添加指标上报"""
        return super().add_view(request, form_url, extra_context)
    
    @metrics.admin_metrics('auth.group.change')
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """修改组的视图，添加指标上报"""
        return super().change_view(request, object_id, form_url, extra_context)
    
    @metrics.admin_metrics('auth.group.delete')
    def delete_view(self, request, object_id, extra_context=None):
        """删除组的视图，添加指标上报"""
        return super().delete_view(request, object_id, extra_context)
    
    @metrics.admin_metrics('auth.group.list')
    def changelist_view(self, request, extra_context=None):
        """组列表视图，添加指标上报"""
        return super().changelist_view(request, extra_context)