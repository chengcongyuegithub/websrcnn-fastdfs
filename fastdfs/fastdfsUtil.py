from fdfs_client.client import Fdfs_client


class Fdfs():
    def __init__(self, client_file):
        self.client = Fdfs_client(client_file)

    def upload(self, upload_file):
        try:
            ret_upload = self.client.upload_by_filename(upload_file)
            file_id = ret_upload['Remote file_id'].replace('\\', '/')
            return file_id

        except Exception as e:
            return None

    def uploadbyBuffer(self, file, suffix):
        try:
            ret_upload = self.client.upload_by_buffer(file, suffix)
            file_id = ret_upload['Remote file_id'].replace('\\', '/')
            return file_id
        except Exception as e:
            print(e)
            return None

    def downloadbyBuffer(self, file_id):
        try:
            ret_download = self.client.download_to_buffer(file_id)
            ret_content = ret_download['Content']
            return ret_content
        except Exception as e:
            return None

    def download(self, download_file, file_id):
        try:
            ret_download = self.client.download_to_file(download_file, file_id)
            ret_content=ret_download['Content']
            return ret_content
        except Exception as e:
            return None

    def delete(self, file_id):
        try:
            ret_delete = self.client.delete_file(file_id)
            return ret_delete
        except Exception as e:
            return None

