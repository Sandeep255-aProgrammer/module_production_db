from werkzeug.utils import secure_filename
import os
from database_table import (
    db ,
    User,
    Station ,
    MaterialReceiverTable,
    VisualInspectionSensorTable,
    VisualInspectionHybridTable,
    VisualInspectionBridgeTable,
    KaptonGluingTable,
    HvIvFormTable,
    SensorGluingTable,
    NeedleMetrologyTable,
    SkeletonTestTable,
    HybridGluingTable,
    ModuleDataTable,
    WireBondingTable,
    NoiseTestTable,
    BurNimTable
)
class SaveToDataBase:
    def __init__(self) -> None:
        # Initialize the database connection (just a placeholder for now)
        self.db_connection = None

    def save_material_receiver_form(self, form):
        pass

    def save_visual_inspection_sensor_form(self, form):
        pass

    def save_visual_inspection_hybrid_form(self, form):
        pass

    def save_visual_inspection_bridge_form(self, form ,db ,file_dir):
        bridge_id = form.bridge_id.data
        bridge_image = form.bridge_image.data
        comment = form.comment.data
        image_url = self.save_get_file_url(bridge_image,file_dir)
        new_bridge_inspection = VisualInspectionBridgeTable(
                                          bridge_id = bridge_id,
                                          bridge_image = image_url,
                                          comment = comment )
        db.session.add(new_bridge_inspection)
        db.session.commit()

    def save_wire_bonding_form(self,form , db , file_dir):
        pass 

    def save_kapton_gluing_form(self, form,db,file_dir):
        sensor_id = form.sensor_id.data
        sensor_type = form.sensor_type.data
        cooling_points = form.cooling_points.data
        part_A_batch_no = form.part_A_batch_no.data
        part_A_exp_date = form.part_A_exp_date.data
        part_B_batch_no = form.part_B_batch_no.data
        part_B_exp_date = form.part_B_exp_date.data
        main_bridge_type = form.main_bridge_type.data
        main_bridge_id = form.main_bridge_id.data
        stump_bridge_type =form.stump_bridge_type.data
        stump_bridge_id = form.stump_bridge_id.data
        image = form.image.data
        comment = form.comment.data

        # Handle file upload for image
        if image:
            image_url = self.save_get_file_url(image,file_dir)
        else:
            image_url = None  # No image uploaded

        # Create a new record in KaptonGluingTable
        new_kapton_gluing = KaptonGluingTable(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            cooling_points=cooling_points,
            part_A_batch_no=part_A_batch_no,
            part_A_exp_date=part_A_exp_date,
            part_B_batch_no=part_B_batch_no,
            part_B_exp_date=part_B_exp_date,
            main_bridge_type = main_bridge_type,
            main_bridge_id = main_bridge_id,
            stump_bridge_type =stump_bridge_type,
            stump_bridge_id = stump_bridge_id,
            image_url=image_url,
            comment=comment
        )   
        db.session.add(new_kapton_gluing)
        db.session.commit()
   
    def save_hv_iv_form(self, form, db, file_dir):
        # Extract form data
        sensor_id = form.sensor_id.data
        sensor_type = form.sensor_type.data
        cooling_points = form.cooling_points.data
        hv_plot = form.hv_plot.data
        iv_plot = form.iv_plot.data
        csv_file = form.csv_file.data
        image = form.image.data
        comment = form.comment.data

        hv_plot_url = self.save_get_file_url(hv_plot,file_dir)
        iv_plot_url = self.save_get_file_url(iv_plot,file_dir)
        csv_url = self.save_get_file_url(csv_file,file_dir)
   
        if image:
            image_url = self.save_get_file_url(image,file_dir)
        else:
            image_url = None

        new_hv_iv_record = HvIvFormTable(
            
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            cooling_points=cooling_points,
            hv_plot_url=hv_plot_url,
            iv_plot_url=iv_plot_url,
            csv_url=csv_url,
            image_url=image_url,
            comment=comment
        )
        db.session.add(new_hv_iv_record)
        db.session.commit()
    def save_sensor_gluing_form(self, form, db, file_dir):
        bare_module_id = form.bare_module_id.data
        top_sensor_id = form.top_sensor_id.data
        bottom_sensor_id = form.bottom_sensor_id.data
        main_bridge = form.main_bridge.data
        stump_bridge = form.stump_bridge.data
        module_spacing = form.module_spacing.data
        cooling_points = form.cooling_points.data
        jigs = form.jigs.data
        part_A_batch_no = form.part_A_batch_no.data
        part_A_exp_date = form.part_A_exp_date.data
        part_B_batch_no = form.part_B_batch_no.data
        part_B_exp_date = form.part_B_exp_date.data
        image = form.image.data
        comment = form.comment.data

        if image:
            image_url = self.save_get_file_url(image,file_dir)
        else:
            image_url = None  
        new_sensor_gluing = SensorGluingTable(
            bare_module_id=bare_module_id,
            top_sensor=top_sensor_id,
            bottom_sensor=bottom_sensor_id,
            main_bridge=main_bridge,
            stump_bridge=stump_bridge,
            module_spacing=module_spacing,
            cooling_points=cooling_points,
            jigs=jigs,
            part_A_batch_no=part_A_batch_no,
            part_A_exp_date=part_A_exp_date,
            part_B_batch_no=part_B_batch_no,
            part_B_exp_date=part_B_exp_date,
            image_url=image_url,
            comment=comment,
        
        )

        db.session.add(new_sensor_gluing)
        db.session.commit()
    
    def save_needle_metrology_form(self, form, db, file_dir):
        # Extract form data
        bare_module_id = form.bare_module_id.data
        x_coordinate = form.x_coordinate.data
        y_coordinate = form.y_coordinate.data
        del_theta = form.del_theta.data
        csv_xl_file = form.csv_xl.data
        image_file = form.image.data
        comment = form.comment.data
        csv_xl_url = self.save_get_file_url(csv_xl_file,file_dir)
        if image_file:
            image_url = self.save_get_file_url(image_file,file_dir)
        else:
            image_url = None  # No image uploaded

        # Create a new record in NeedleMetrologyTable
        new_needle_metrology = NeedleMetrologyTable(
            bare_module_id=bare_module_id,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            del_theta=del_theta,
            csv_xl_url=csv_xl_url,
            image_url=image_url,
            comment=comment,
        )

        db.session.add(new_needle_metrology)
        db.session.commit()

    def save_skeleton_test_form(self, form, db, file_dir):
        skeleton_id = form.skeleton_id.data
        FEH_L = form.FEH_L.data
        FEH_R = form.FEH_R.data
        VTRx = form.VTRx.data
        ground_balancer_id = form.ground_balancer_id.data
        comment = form.comment.data
        root_file = form.root_file.data
        root_file_url = self.save_get_file_url(root_file,file_dir)
        new_skeleton_test = SkeletonTestTable(
            skeleton_id=skeleton_id,
            FEH_L=FEH_L,
            FEH_R=FEH_R,
            VTRx=VTRx,
            ground_balancer_id=ground_balancer_id,
            root_file_url=root_file_url,
            comment=comment,
        )
        db.session.add(new_skeleton_test)
        db.session.commit()
    def save_hybrid_gluing_form(self, form ,db ,file_dir):
        module_id = form.module_id.data
        bare_module_id = form.bare_module_id.data
        skeleton_id = form.skeleton_id.data
        part_A_batch_no = form.part_A_batch_no.data
        part_A_exp_date = form.part_A_exp_date.data
        part_B_batch_no = form.part_B_batch_no.data
        part_B_exp_date = form.part_B_exp_date.data
        image = form.image.data
        comment = form.comment.data
        if form.image.data:
            image_url = self.save_get_file_url(image,file_dir)
        else:
            image_url = None  
        new_record = HybridGluingTable(
            module_id=module_id,
            bare_module_id=bare_module_id,
            skeleton_id=skeleton_id,
            part_A_batch_no=part_A_batch_no,
            part_A_exp_date=part_A_exp_date,
            part_B_batch_no=part_B_batch_no,
            part_B_exp_date=part_B_exp_date,
            image_url=image_url,
            comment=comment,
        )

        db.session.add(new_record)
        db.session.commit()
    def save_module_data_form(self, form):
        pass

    def save_wire_bonding_form(self, form):
        pass
    def save_burnim_test_form(self, form, db, file_dir, module_quantity):
        # Get the form data
        burnim_box_result = form.burnim_box_result.data
        comment = form.comment.data
        
        # Save the burnim box result file if uploaded
        if burnim_box_result:
            burnim_box_result_url = self.save_get_file_url(burnim_box_result, file_dir)
        else:
            burnim_box_result_url = None
        
        # Initialize the values for the dynamic modules and their test files
        module_data = {}
        
        for i in range(1, module_quantity + 1):
            module_id_field = getattr(form, f"module{i}_id", None)
            module_result_field = getattr(form, f"module{i}_result", None)
            
            if module_id_field and module_result_field:
                module_id = module_id_field.data
                module_result_file = module_result_field.data
                
                # Save the module result file and get the file URL
                if module_result_file:
                    module_result_file_url = self.save_get_file_url(module_result_file, file_dir)
                else:
                    module_result_file_url = None
                
                module_data[f"module{i}_id"] = module_id
                module_data[f"module{i}_test_file"] = module_result_file_url
        
        # Save the image URL if an image is uploaded
        image_url = None
        if form.image.data:
            image_url = self.save_get_file_url(form.image.data, file_dir)
        
        # Create a new record and populate it with the form data and dynamically gathered module data
        new_record = BurNimTable(
            burnim_box_result=burnim_box_result_url,
            comment=comment,
            image_url=image_url,
            module_quantity = module_quantity
        )
        
        # Add the dynamically gathered module data (module IDs and test files) to the new record
        for module_key, module_value in module_data.items():
            setattr(new_record, module_key, module_value)
        
        # Add the new record to the database session and commit it
        db.session.add(new_record)
        db.session.commit()
    def save_noise_test_form(self, form):
        pass

    def save_to_table(self, table_name, form):
        pass
    def save_get_file_url(self ,file,file_dir):
        filename = secure_filename(file.filename)
        file_path = os.path.join(file_dir,filename)
        # while saving if the dir contain the save filename then that might cretae some problem fix it
        file.save(file_path)
        return file_path

