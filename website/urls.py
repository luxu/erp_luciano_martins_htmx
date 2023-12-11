from django.urls import include, path

from . import views

# from . import views_gasto_segmento as v_gastos

app_name = "website"

# pecas_crud = [
#     path(
#         "",
#         views.PecasListView.as_view(),
#         name="website_pecas_list",
#     ),
#     path(
#         "website/pecas/create/",
#         views.PecasCreateView.as_view(),
#         name="website_pecas_create",
#     ),
#     path(
#         "website/pecas/<int:pk>/edit/",
#         views.PecasEditView.as_view(),
#         name="website_pecas_edit",
#     ),
#     path(
#         "website/pecas/<int:pk>/delete/",
#         views.PecasDeleteView.as_view(),
#         name="website_pecas_delete",
#     ),
#     path(
#         "website/pecas/import/",
#         views.import_pecas,
#         name="website_pecas_import",
#     ),
#     path(
#         "website/pecas/pecas_import_pecas/",
#         views.pecas_import_pecas,
#         name="website_pecas_process_import",
#     ),
#     path(
#         "website/itenspecas/<int:pk>/details/",
#         views.ItensPecasDetailView.as_view(),
#         name="website_itenspecas_detail",
#     ),
# ]

# events_crud = [
#     path(
#         "",
#         views.EventsListView.as_view(),
#         name="website_events_list",
#     ),
#     path(
#         "create/",
#         views.EventsCreateView.as_view(),
#         name="website_events_create",
#     ),
#     path(
#         "<int:pk>/edit/",
#         views.EventsEditView.as_view(),
#         name="website_events_edit",
#     ),
#     path(
#         "<int:pk>/delete/",
#         views.EventsDeleteView.as_view(),
#         name="website_events_delete",
#     ),
#     path(
#         "autocomplete/",
#         views.AutoCompleteView.as_view(),
#         name="website_events_autocomplete",
#     ),
# ]
#
# vivo_crud = [
#     path(
#         "",
#         views.VivoListView.as_view(),
#         name="website_vivo_list",
#     ),
#     path(
#         "website/vivo/create/",
#         views.VivoCreateView.as_view(),
#         name="website_vivo_create",
#     ),
#     path(
#         "website/vivo/criar/",
#         views.model_form_upload,
#         name="website_vivo_criar",
#     ),
#     path(
#         "website/vivo/<int:pk>/edit/",
#         views.VivoEditView.as_view(),
#         name="website_vivo_edit",
#     ),
#     path(
#         "website/vivo/<int:pk>/delete/",
#         views.VivoDeleteView.as_view(),
#         name="website_vivo_delete",
#     ),
# ]

city_crud = [
    path(
        "",
        views.CityListView.as_view(),
        name="localization_list",
    ),
    path(
        "search/",
        views.CitySearchView,
        name="localization_search",
    ),
    path(
        "create/",
        views.CityCreateView.as_view(),
        name="localization_create",
    ),
    path("<int:pk>/", views.CityDetailsView.as_view(), name="localization_detail"),
    path(
        "<int:pk>/edit/",
        views.CityEditView.as_view(),
        name="localization_update",
    ),
    path(
        "<int:pk>/delete/",
        views.CityDeleteView.as_view(),
        name="localization_delete",
    ),
]

# comercio_crud = [
#     path(
#         "",
#         views.ComercioListView.as_view(),
#         name="website_comercio_list",
#     ),
#     path(
#         "website/comercio/create/",
#         views.ComercioCreateView.as_view(),
#         name="website_comercio_create",
#     ),
#     path(
#         "website/comercio/<int:pk>/edit/",
#         views.ComercioEditView.as_view(),
#         name="website_comercio_edit",
#     ),
#     path(
#         "website/comercio/<int:pk>/delete/",
#         views.ComercioDeleteView.as_view(),
#         name="website_comercio_delete",
#     ),
#     path(
#         "website/comercio/import/",
#         views.import_comercio,
#         name="website_comercio_import",
#     ),
# ]
#
# skills_crud = [
#     path(
#         "",
#         views.SkillsListView.as_view(),
#         name="website_skills_list",
#     ),
#     path(
#         "website/skills/create/",
#         views.SkillsCreateView.as_view(),
#         name="website_skills_create",
#     ),
#     path(
#         "website/skills/<int:pk>/edit/",
#         views.SkillsEditView.as_view(),
#         name="website_skills_edit",
#     ),
#     path(
#         "website/skills/<int:pk>/delete/",
#         views.SkillsDeleteView.as_view(),
#         name="website_skills_delete",
#     ),
# ]
#
# empresa_crud = [
#     path(
#         "",
#         views.EmpresaListView.as_view(),
#         name="website_empresa_list",
#     ),
#     path(
#         "website/empresa/create/",
#         views.EmpresaCreateView.as_view(),
#         name="website_empresa_create",
#     ),
#     path(
#         "website/empresa/<int:pk>/edit/",
#         views.EmpresaEditView.as_view(),
#         name="website_empresa_edit",
#     ),
#     path(
#         "website/empresa/<int:pk>/delete/",
#         views.EmpresaDeleteView.as_view(),
#         name="website_empresa_delete",
#     ),
#     path(
#         "website/empresa/<int:pk>/detail/",
#         views.EmpresaDetailView.as_view(),
#         name="website_empresa_details",
#     ),
# ]
#
# emprego_crud = [
#     path(
#         "",
#         views.EmpregoListView.as_view(),
#         name="website_emprego_list",
#     ),
#     path(
#         "website/emprego/create/",
#         views.EmpregoCreateView.as_view(),
#         name="website_emprego_create",
#     ),
#     path(
#         "website/emprego/<int:pk>/edit/",
#         views.EmpregoEditView.as_view(),
#         name="website_emprego_edit",
#     ),
#     path(
#         "website/emprego/<int:pk>/detail/",
#         views.EmpregoDetailView.as_view(),
#         name="website_emprego_details",
#     ),
#     path(
#         "website/emprego/<int:pk>/delete/",
#         views.EmpregoDeleteView.as_view(),
#         name="website_emprego_delete",
#     ),
# ]
#
# consultancy_crud = [
#     path(
#         "",
#         views.ConsultancyListView.as_view(),
#         name="website_consultancy_list",
#     ),
#     path(
#         "website/consultancy/create/",
#         views.ConsultancyCreateView.as_view(),
#         name="website_consultancy_create",
#     ),
#     path(
#         "website/consultancy/<int:pk>/edit/",
#         views.ConsultancyEditView.as_view(),
#         name="website_consultancy_edit",
#     ),
#     path(
#         "website/consultancy/<int:pk>/delete/",
#         views.ConsultancyDeleteView.as_view(),
#         name="website_consultancy_delete",
#     ),
# ]
#
# cartoes_crud = [
#     path(
#         "",
#         v_gastos.CardbankListView.as_view(),
#         name="website_cartoes_list",
#     ),
#     path(
#         "website/cartoes/create/",
#         v_gastos.CardbankCreateView.as_view(),
#         name="website_cardbank_create",
#     ),
#     path(
#         "website/cartoes/<int:pk>/edit/",
#         v_gastos.CardbankEditView.as_view(),
#         name="website_cardbank_edit",
#     ),
#     path(
#         "website/cartoes/<int:pk>/delete/",
#         v_gastos.CardbankDeleteView.as_view(),
#         name="website_cardbank_delete",
#     ),
# ]
#
# chatgpt_crud = [
#     path(
#         "",
#         views.ChatgptListView.as_view(),
#         name="website_chatgpt_list",
#     ),
#     path(
#         "website/chatgpt/create/",
#         views.EventsCreateView.as_view(),
#         name="website_chatgpt_create",
#     ),
#     path(
#         "website/chatgpt/<int:pk>/edit/",
#         views.EventsEditView.as_view(),
#         name="website_chatgpt_edit",
#     ),
#     path(
#         "website/chatgpt/<int:pk>/delete/",
#         views.EventsDeleteView.as_view(),
#         name="website_chatgpt_delete",
#     ),
# ]

urlpatterns = [
    # path("pecas/", include(pecas_crud)),
    # path("events/", include(events_crud)),
    # path("comercio/", include(comercio_crud)),
    path("localization/", include(city_crud)),
    # path("consultancy/", include(consultancy_crud)),
    # path("emprego/", include(emprego_crud)),
    # path("empresa/", include(empresa_crud)),
    # path("skills/", include(skills_crud)),
    # path("vivo/", include(vivo_crud)),
    # path("cartoes/", include(cartoes_crud)),
    # path("chatgpt/", include(chatgpt_crud)),
]
