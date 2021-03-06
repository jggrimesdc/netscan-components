import os
from scan_api_lib import WCaaSUtils


def main(event, context):
    bucket = os.environ.get("BUCKET")
    cluster_id = os.environ.get("CLUSTER_ID")
    cluster_name = os.environ.get("CLUSTER_NAME")

    pod_ips = WCaaSUtils.get_cassandra_pod_ips(cluster_name, cluster_id)

    event['detail']['sparkargs'] = []
    event['detail']['sparkargs'].append("spark-submit")
    event['detail']['sparkargs'].append(f"s3://{bucket}/scripts/emr_iihd_processor.py")
    event['detail']['sparkargs'].append("--bucketName")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("bucket", {}).get("name"))
    event['detail']['sparkargs'].append("--objectKey")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("object", {}).get("key"))
    event['detail']['sparkargs'].append("--fileSource")
    event['detail']['sparkargs'].append(event["detail"].get("file_source"))
    event['detail']['sparkargs'].append("--cassandraHost")
    event['detail']['sparkargs'].append(pod_ips[0])
    event['detail']['sparkargs'].append("--jar")
    event['detail']['sparkargs'].append("spark-cassandra-connector-assembly-2.5.1.jar")

    return event
