from django import forms
from .models import medico, paciente, cita
import datetime

class MedicoForm(forms.ModelForm):
    class Meta:
        model = medico
        fields = ['nombre', 'rut', 'especialidad', 'telefono', 'correo']    
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        metadata = {
            'ordering': ['nombre', 'especialidad', 'rut', 'telefono', 'correo'],

        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = paciente
        fields = ['nombre', 'rut', 'fecha_nacimiento', 'telefono', 'correo']    
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': datetime.date.today().strftime('%Y-%m-%d')}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        metadata = {
            'ordering': ['nombre', 'rut', 'fecha_nacimiento', 'telefono', 'correo'],
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = cita
        fields = ['paciente', 'medico', 'especialidad', 'fecha_cita', 'hora_cita', 'observaciones']    
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}),
            'hora_cita': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        metadata = {
            'ordering': ['paciente', 'medico', 'especialidad', 'fecha_cita', 'hora_cita', 'observaciones'],
        }

    def clean_fecha_cita(self):
        fecha_cita = self.cleaned_data['fecha_cita']
        if fecha_cita < datetime.date.today():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha_cita
    
    def clean(self):
        cleaned_data = super().clean()
        medico_selected = cleaned_data.get('medico')
        fecha_cita = cleaned_data.get('fecha_cita')
        hora_cita = cleaned_data.get('hora_cita')

        if medico_selected and fecha_cita and hora_cita:
            if cita.objects.filter(medico=medico_selected, fecha_cita=fecha_cita, hora_cita=hora_cita).exists():
                raise forms.ValidationError("El médico ya tiene una cita programada para esta fecha y hora.")
        return cleaned_data
    
    
    
    