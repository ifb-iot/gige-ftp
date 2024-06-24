
import time
import os
import tempfile
import stapipy as st
import datetime
number_of_images_to_grab = 1
tempfile.tempdir = "./uploads"

st.initialize()
st_system = st.create_system()
st_device = st_system.create_first_device()
print('Device=', st_device.info.display_name)
st_datastream = st_device.create_datastream()

def Process_img():
    try:
        st_datastream.start_acquisition(number_of_images_to_grab)
        st_device.acquisition_start()
        current_time = datetime.datetime.now()
        filename = current_time.strftime("%Y%m%d%H%M%S") 
        filename_prefix = filename
        file_location = os.path.join(tempfile.gettempdir(),
                                    filename_prefix + ".png")
        print("file_location" ,file_location )

        is_image_saved = False
        with st_datastream.retrieve_buffer() as st_buffer:
            if st_buffer.info.is_image_present:
                st_image = st_buffer.get_image()
                st_stillimage_filer = st.create_filer(st.EStFilerType.StillImage)
                print("Saving {0} ... ".format(file_location), end="")
                st_stillimage_filer.save(st_image,
                    st.EStStillImageFileFormat.StApiRaw, file_location)
                print("done.")
                is_image_saved = True
            else:
                print("Image data does not exist.")

        st_device.acquisition_stop()
        st_datastream.stop_acquisition()


    except Exception as exception:
        print(exception)


def measure_processing_time(num_iterations=10):
    total_time = 0
    iteration_times = []

    for _ in range(num_iterations):
        start_time = time.time()  
        Process_img()
        end_time = time.time()
        iteration_time = end_time - start_time
        iteration_times.append(iteration_time)
        total_time += iteration_time
        print(f"Time taken for this iteration: {iteration_time:.4f} seconds")

    # Print the total time taken and the average time per iteration
    print(f"\nTotal time for {num_iterations} iterations: {total_time:.4f} seconds")
    print(f"Average time per iteration: {total_time / num_iterations:.4f} seconds")

# Call the measure_processing_time function
measure_processing_time()