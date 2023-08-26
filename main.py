import os
from obspy import read, read_inventory
from obspy.clients.neic import Client

def remove_response_and_save_mseed(input_dir, output_dir, metadata_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all MiniSEED files in the input directory
    for filename in os.listdir(input_dir):
        print(f"{filename}")
        # if filename.endswith(".mseed"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Load MiniSEED file
        st = read(input_path)

        # Load corresponding metadata
        network = st[0].stats.network
        station = st[0].stats.station
        location = st[0].stats.location
        channel = st[0].stats.channel

        # print(f"    {network}.{station}.{location}.{channel}.xml")
        metadata_path = os.path.join(metadata_dir, f"{network}.{station}.{location}.{channel}.xml")

        # Dataless
        # metadata_path = os.path.join(metadata_dir, "out4.response.restored-EHZ-plus-decimation.dataless-new")

        # Seiscomp
        # metadata_path = os.path.join(metadata_dir, "out4.response.restored-EHZ-plus-decimation-new")


        inv = read_inventory(metadata_path,level="network")

        # Remove instrument response
        st.remove_response(inventory=inv, output="ACC")

        # Save the processed stream as MiniSEED
        st.write(output_path, format="MSEED")

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(),"in")
    output_directory = os.path.join(os.getcwd(),"out")
    metadata_directory = os.path.join(os.getcwd(),"metadata")

    remove_response_and_save_mseed(input_directory, output_directory, metadata_directory)
