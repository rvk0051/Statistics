from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Max, Min
from .models import PlacedStudent, Company
from django.conf import settings
from .utils import calculate_salary_distribution  # Import the function
def placement_stats(request):
    """Render the placement stats page."""
    return render(request, 'placement_stats.html')

def get_chart_data(request):
    """Fetch placement statistics filtered by company and branch."""
    
    selected_company = request.GET.get('company', None)
    selected_branch = request.GET.get('branch', None)

    # Default company: the one offering the highest salary
    highest_salary_company = PlacedStudent.objects.order_by('-salary_lpa').first()
    default_company = highest_salary_company.company.name if highest_salary_company else None

    # Get all companies for the dropdown
    all_companies = list(Company.objects.values_list('name', flat=True).distinct())

    # Get all branches and ensure "All Branches" is the first option
    all_branches = ["All Branches"] + list(PlacedStudent.objects.values_list('branch', flat=True).distinct())

    # If no company is selected, use the default one
    if not selected_company:
        selected_company = default_company

    # Apply filters
    filters = {'company__name': selected_company} if selected_company else {}

    # Ensure proper filtering when selecting a specific branch
    if selected_branch and selected_branch != "All Branches":
        filters['branch'] = selected_branch  

    # Query to get placement data
    company_placement_data = list(
        PlacedStudent.objects.filter(**filters)
        .values('placement_year')
        .annotate(students_placed=Count('student_id'))
        .order_by('placement_year')
    )

    return JsonResponse({
        'company_placement_data': company_placement_data,
        'companies': all_companies,
        'branches': all_branches,  # Now includes "All Branches"
        'default_company': default_company,
        'selected_company': selected_company,
        'selected_branch': selected_branch if selected_branch else "All Branches"
    })


def get_salary_distribution(request):
    """Fetch salary distribution dynamically with 10 LPA steps."""
    selected_branch = request.GET.get('branch', None)
    selected_year = request.GET.get('year', None)

    # Default filters
    filters = {}
    if selected_branch:
        filters['branch'] = selected_branch
    if selected_year:
        filters['placement_year'] = selected_year

    # Get available branches & years
    all_branches = list(PlacedStudent.objects.values_list('branch', flat=True).distinct())
    all_years = list(PlacedStudent.objects.values_list('placement_year', flat=True).distinct())

    # Fixed Salary Ranges (0-10, 10-20, ...)
    salary_ranges = [(f"{i} - {i+10} LPA", i, i+10) for i in range(0, 100, 10)]  # 0-10, 10-20, ... till 100 LPA

    salary_distribution = []
    for label, min_range, max_range in salary_ranges:
        count = PlacedStudent.objects.filter(**filters, salary_lpa__gte=min_range, salary_lpa__lt=max_range).count()
        salary_distribution.append({'salary_range': label, 'students_count': count})

    total_placed_students = sum(item['students_count'] for item in salary_distribution)

    return JsonResponse({
        'salary_distribution': salary_distribution,
        'total_placed_students': total_placed_students,
        'branches': all_branches,
        'years': all_years
    })


def get_top_achievers(request):
    top_achievers = (
        PlacedStudent.objects.values('placement_year')
        .annotate(max_salary=Max('salary_lpa'))
        .order_by('-placement_year')
    )

    achievers_data = []
    for achiever in top_achievers:
        student = PlacedStudent.objects.filter(
            placement_year=achiever['placement_year'],
            salary_lpa=achiever['max_salary']
        ).first()

        if student:
            if student.photo:
               photo_url = student.photo.url
            else:
                photo_url = f"{settings.MEDIA_URL}achievers/Designer(1).png"

            achievers_data.append({
                'year': student.placement_year,
                'student_name': student.student_name,
                'company': student.company.name,
                'salary_lpa': student.salary_lpa,
                'photo': photo_url,
            })

    return JsonResponse({'top_achievers': achievers_data})
