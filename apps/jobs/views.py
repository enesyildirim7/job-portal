import re
from turtle import up
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from apps.jobs.filters import JobFilter
from apps.jobs.models import Jobs
from apps.users.models import User
from taggit.models import Tag
from apps.jobs.forms import CreateJobForm, UpdateJobForm

@login_required
def create_job(request):
    """İş ilanı oluşturma"""

    form = CreateJobForm(request.POST or None)

    context = {"form": form}

    if form.is_valid():
        job = form.save(commit=False)
        job.ilan_sahibi = request.user
        job.save()
        form.save_m2m()
        messages.success(request, "İş ilanı oluşturuldu.")

        return redirect(f"/jobs/{job.id}")

    return render(request, "pages/createjob.html", context)


@login_required
def edit_job(request,id):
    """İş ilanı güncelleme"""

    job = get_object_or_404(Jobs, id=id)

    if request.method == "POST":
        update_form = UpdateJobForm(request.POST, instance=job)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "İlan güncellendi.")
            return redirect(f"/jobs/{job.id}")
    
    update_form = UpdateJobForm(instance=job)

    return render(request, "pages/edit-job.html", {"form":update_form,"id":id})



def job_list(request):
    """Tüm iş ilanları listesi"""

    f = JobFilter(request.GET, queryset=Jobs.objects.all())

    return render(request, "pages/jobs.html", {"jobs":f})


@login_required
def delete_job(request,id):
    """İş ilanını silme"""

    job = get_object_or_404(Jobs, id=id)
    job.delete()
    messages.success(request, "İş ilanı silindi.")

    return redirect("jobs:list")


def detail_job(request,id):
    """İş ilanı detayları"""

    authenticate = True
    job = get_object_or_404(Jobs,id=id)
    basvuranlar = job.adaylar.all()
    apply = False
    save = False
    if request.user.id is not None:
        user = User.objects.get(id=request.user.id)
        if job in user.basvurulan_ilanlar.all():
            apply = True

        if job in user.kaydedilen_ilanlar.all():
            save=True
    else:
        authenticate = False
    
    context = {
        "job": job,
        "apply":apply,
        "save":save,
        "authenticate":authenticate,
        "basvuranlar":basvuranlar
    }

    return render(request, "pages/job-detail.html", context)


@login_required
def apply_job(request,id):
    """İş başvurusu"""

    job = get_object_or_404(Jobs,id=id)
    user = User.objects.get(id=request.user.id)
    user.basvurulan_ilanlar.add(job)

    job.adaylar.add(user)

    messages.success(request, f"{job.baslik} ilanına başvurunuz gerçekleştirildi.")

    return redirect(f"/jobs/{id}")


@login_required
def save_job(request,id):
    """İş kaydet"""

    job = get_object_or_404(Jobs, id=id)
    user = User.objects.get(id=request.user.id)
    user.kaydedilen_ilanlar.add(job)

    messages.success(request, "İlan kaydedildi.")

    return redirect(f"/jobs/{id}")


@login_required
def unsave_job(request,id):
    """İş kaydet"""

    job = get_object_or_404(Jobs,id=id)
    user = User.objects.get(id=request.user.id)
    user.kaydedilen_ilanlar.remove(job)

    messages.success(request, "İlan kayıttan çıkarıldı.")

    return redirect(f"/jobs/{id}")
