from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        report_type = request.form.get('report_type', 'general')
        
        patient_data = {
            'inv_date': request.form.get('inv_date'),
            'print_date': request.form.get('print_date'),
            'id_no': request.form.get('id_no'),
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'refd_by': request.form.get('refd_by'),
            'lab_incharge': request.form.get('lab_incharge'),
            'pathologist': request.form.get('pathologist'),
            'report_type': report_type
        }

        if report_type == 'creatinine':
            patient_data['creatinine_val'] = request.form.get('creatinine_val')
            patient_data['creatinine_unit'] = request.form.get('creatinine_unit', 'mg/dl')
            patient_data['creatinine_range'] = request.form.get('creatinine_range', '0.55 - 1.30')

        elif report_type == 'crp':
            patient_data['crp_val'] = request.form.get('crp_val')
            patient_data['crp_unit'] = request.form.get('crp_unit', 'mg/l')
            patient_data['crp_range'] = request.form.get('crp_range', '< 6.0')

        elif report_type == 'urine_routine':
            patient_data['physical'] = {
                'quantity': request.form.get('u_quantity'),
                'color': request.form.get('u_color'),
                'appearance': request.form.get('u_appearance'),
                'sp_gravity': request.form.get('u_sp_gravity')
            }
            patient_data['chemical'] = {
                'reaction': request.form.get('u_reaction'),
                'sugar': request.form.get('u_sugar'),
                'albumin': request.form.get('u_albumin')
            }
            patient_data['microscopic'] = {
                'pus_cells': request.form.get('u_pus'),
                'rbc': request.form.get('u_rbc'),
                'epithelial': request.form.get('u_epithelial')
            }

        elif report_type == 'urine_pregnancy':
            patient_data['pregnancy_result'] = request.form.get('pregnancy_result')

        elif report_type == 'triple_antigen':
            patient_data['widal_to'] = request.form.get('widal_to')
            patient_data['widal_th'] = request.form.get('widal_th')
            patient_data['widal_ah'] = request.form.get('widal_ah')
            patient_data['widal_bh'] = request.form.get('widal_bh')

        else:
            sections = []
            sec_titles = request.form.getlist('sec_title[]')
            sec_subtitles = request.form.getlist('sec_subtitle[]')

            for idx, title in enumerate(sec_titles):
                if title.strip():
                    t_names = request.form.getlist(f'test_name_{idx}[]')
                    results = request.form.getlist(f'result_{idx}[]')
                    units = request.form.getlist(f'unit_{idx}[]')
                    ranges = request.form.getlist(f'normal_range_{idx}[]')

                    test_list = []
                    for i in range(len(t_names)):
                        if t_names[i].strip():
                            test_list.append({
                                'name': t_names[i],
                                'result': results[i],
                                'unit': units[i],
                                'range': ranges[i]
                            })
                    sections.append({
                        'title': title,
                        'subtitle': sec_subtitles[idx] if idx < len(sec_subtitles) else '',
                        'tests': test_list
                    })
            patient_data['sections'] = sections

        return render_template('report.html', data=patient_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
