from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Max
from .models import PlacedStudent, Company
from .utils import calculate_salary_distribution  # Import the function
def placement_stats(request):
    """Render the placement stats page."""
    return render(request, 'placement_stats.html')

def get_chart_data(request):
    """Fetch company-wise placement statistics and return JSON response."""
    
    selected_company = request.GET.get('company', None)

    # Find the company that offered the highest salary
    highest_salary_company = PlacedStudent.objects.order_by('-salary_lpa').first()
    default_company = highest_salary_company.company.name if highest_salary_company else None

    # Get all company names for the dropdown
    all_companies = list(Company.objects.values_list('name', flat=True).distinct())

    # If no company is selected, use the default company
    if not selected_company:
        selected_company = default_company

    #  Get student placement count **per year** for the selected company
    company_placement_data = list(
        PlacedStudent.objects.filter(company__name=selected_company)
        .values('placement_year')
        .annotate(students_placed=Count('student_id'))
        .order_by('placement_year')
    )

    # Debugging: Print API response
    print("API Response:")
    print("Company Placement Data:", company_placement_data)
    print("Companies List:", all_companies)
    print("Default Company:", default_company)
    print("Selected Company:", selected_company)  # ✅ This avoids errors


    return JsonResponse({
        'company_placement_data': company_placement_data,
        'companies': all_companies,
        'default_company': default_company,
        'selected_company': selected_company
    })

def get_salary_distribution(request):
    salary_data = calculate_salary_distribution()
    return JsonResponse({'salary_distribution': salary_data})

