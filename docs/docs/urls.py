# from django.urls import path
# from .views import *
#
# app_name = 'docs'
#
# urlpatterns = [
#     path('check_progress/', CheckProgressView.as_view(), name='check_progress'),
#     path('export/excel/', ExcelAllView.as_view(), name='zayvki_export_excel'),
#     path('export/excel/classroom/<int:Classroom_id>/', ExcelClassroomView.as_view(), name='excel_classroom'),
#     path('export/dashboard/', ExportExcelView.as_view(), name='export_excel_result'),
#     path('import/users', ImportUsersView.as_view(), name='import_users'),
#     path('import_olympiads/', ImportOlympiadsView.as_view(), name='import_olympiads'),
#     path('download/zip/', CreateZipArchiveView.as_view(), name='download_applications_zip'),
#     path('download/teacher/zip/', CreateZipArchiveForTeacherView.as_view(), name='download_teacher_applications_zip'),
#     path('dashboard/', DashboardView.as_view(), name='dashboard'),
#     path('dashboard/export/', ExportExcelView.as_view(), name='export_excel'),
#     path('import_cpkimr/', import_cpkimr, name='import_cpkimr'),
# ]
