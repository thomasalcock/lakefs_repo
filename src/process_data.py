from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from typing import Tuple
import io
import pandas as pd
import numpy as np
import yaml
import pdb
import logging


def get_cfg(yaml_path: str) -> Tuple[dict, dict]:
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f)
        return cfg["techuser"], cfg["server"]


def setup_client(secrets: dict, server: dict) -> SwaggerClient:
    http_client = RequestsClient()
    http_client.set_basic_auth(
        server["url"],
        secrets["access_key_id"],
        secrets["secret_access_key"],
    )
    client = SwaggerClient.from_url(
        server["local_url"] + "/swagger.json", http_client=http_client
    )

    return client


def get_data(client: SwaggerClient, repo: str, branch: str, path: str) -> pd.DataFrame:
    file_bytes = (
        client.objects.getObject(repository=repo, ref=branch, path=path)
        .response()
        .result
    )

    return pd.read_csv(io.BytesIO(file_bytes), encoding="unicode-escape")


def upload_data(
    df: pd.DataFrame, client: SwaggerClient, repo: str, branch: str, path: str
) -> None:
    df.to_csv(path)
    with open(path, "rb") as file_handler:
        client.objects.uploadObject(
            repository=repo, branch=branch, path=path, content=file_handler
        ).result()


def create_commit(client: SwaggerClient, repo: str, branch: str, msg: str) -> None:
    client.commits.commit(
        repository=repo, branch=branch, commit={"message": msg}
    ).result()


def clean_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    names = df.columns
    df.columns = [x.lower() for x in names]
    return df


def normalize(df: pd.DataFrame, col: list) -> pd.DataFrame:
    df = df.copy()
    col_new = f"{col}_transformed"
    df[col_new] = (df[col] - np.mean(df[col])) / np.std(df[col])
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Get config")
    secrets, server = get_cfg(".lakectl.yaml")
    logging.info("Setup client")
    main_client = setup_client(secrets, server)
    logging.info("Get data")
    df = get_data(main_client, "new-repo", "master", "sales_data_sample.csv")
    logging.info("Transform data")
    df = clean_cols(df)
    df_new = df.iloc[:, 0:8]
    df_new = normalize(df_new, "priceeach")
    df_new = normalize(df_new, "quantityordered")
    df_new = normalize(df_new, "sales")
    logging.info("Upload data")
    # upload_data(df_new, main_client, "new-repo", "dev", "data/sales_transformed.csv")
    logging.info("Create new commit")
    # create_commit(main_client, "new-repo", "dev", "Transform sales, revenue")
