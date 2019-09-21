from rest_framework.response import Response
from rest_framework import status, views
from rest_framework import authentication, permissions
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from .models import Report
from .serializers import ReportSerializer

types_supported = ['sum', 'mul', 'sub', 'div']
complex_types_supported = ['pow', 'sqroot', 'fact']


def sum(num1, num2):
    return num1 + num2


def sub(num1, num2):
    return num1 - num2


def mul(num1, num2):
    return num1 * num2


def div(num1, num2):
    return num1 / num2


def pow(num1, num2):
    out = 1
    for i in range(num2):
        out = out * num1
    return out


def sqroot(*num):
    import math
    return math.sqrt(num[0])


def fact(*num):
    fact = 1
    for i in range(num[0], 0, -1):
        fact = fact * i
    return fact


class CalculateAPI(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def _add_to_report(self, **kwargs):
        report = Report.objects.create(
            user=kwargs['user'],
            operation_type=kwargs['operation_type'])
        report.operands = str(kwargs['num1'])
        if kwargs.get('num2'):
            report.operands = report.operands + ', ' + str(kwargs['num2'])
        report.result = kwargs['result']
        report.save()
        return report

    def post(self, request, *args, **kwargs):
        if request.data:
            operation_type = request.data.get('type')
            num1 = request.data.get('num1')
            num2 = request.data.get('num2', '')

            if operation_type in complex_types_supported and \
                    request.user.groups.filter(name='admin').exists():
                result = eval(operation_type)(num1, num2)
            elif operation_type in types_supported:
                result = eval(operation_type)(num1, num2)
            else:
                return HttpResponseForbidden('can not perform this action')

            report = self._add_to_report(
                user=request.user,
                operation_type=operation_type,
                num1=num1,
                num2=num2,
                result=result
            )
            return Response(result)
        return Response(status.HTTP_400_BAD_REQUEST)


class ReportAPI(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        if request.data:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            reports = Report.objects.filter(date__gte=start_date,
                                            date__lte=end_date)
            serializer = ReportSerializer(reports, many=True)

            return JsonResponse(serializer.data, safe=False)
