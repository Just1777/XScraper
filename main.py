import asyncio
import csv
import os
from datetime import datetime
from twscrape import API, gather


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def user_to_dict(user):
    """Convertit un objet User twscrape en dict propre pour CSV."""
    return {
        "id": user.id,
        "username": user.username,
        "displayname": user.displayname,
        "followers": user.followersCount,
        "created_at": user.created.isoformat() if user.created else None
    }


async def main():

    api = API("account.db")

    await api.pool.delete_accounts("adeline_po62899")

    cookies = (
        "__cf_bm=XHMB2tb2zLMgujAmguKxm9tdEVesGM9R5S8y_bJ2oy0-1764064486.3513713-1.0.1.1-U4lMl4iMyhaXGINiVhXzuSd0e_Nb1nfoK1wR_nbmL1.z5ysKLdToOj7b5pFJQH0A2EMtOw3hUB0OyFpz9G8l_3uwV7waMHIrRy2fxmtpHByIWw5HDFX8g8CjJLLBYsIA; "
        "__cuid=2344b95d4b7a410db93cbed7c9dad636; "
        "auth_multi=\"1163814248159444992:cdc668e1e8163b5b04a08960c7313e979998d55c\"; "
        "auth_token=6c83f953471ad21f4b7dde891385fd8f8b30f0ea; "
        "ct0=f40135ee185efaca155690db6d8da1983429aed8abd66c7998f3b0f37730a53be36aefe14886e602fe1181bc11c2165fcc2196056b7bf17ce05ed8cb76e7fb21d833744369b0012af74ef00fd1e7a18f; "
        "d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; "
        "des_opt_in=N; "
        "dnt=1; "
        "g_state={\"i_l\":0,\"i_ll\":1764064225280}; "
        "gt=1993255932273295826; "
        "guest_id=v1%3A176406431785159207; "
        "kdt=Q62JWOokgKT8DWJbncprkn0eCbv2CeERlw6h3u5L; "
        "lang=fr; "
        "twid=u%3D1991931663044255744; "
        "twtr_pixel_opt_in=N"
    )

    await api.pool.add_account(
        "adeline_po62899",
        "AdelinePotierLaFolle#1",
        "u6592933675@gmail.com",
        "rExky4-riwxyb-jybfeh",
        cookies=cookies
    )

    await api.pool.login_all()

    # ---------- Scrapping ----------
    user_id = 1163814248159444992
    limits = 49
    output_dir = "data/raw"
    ensure_dir(output_dir)

    print(f"Scraping '{user_id}' ...")

    users = await gather(api.followers(user_id, limit=limits))

    print(f"Utilisateurs récupérés : {len(users)}")

    # ---------- Sauvegarde ----------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_dir}/users_{timestamp}.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(user_to_dict(users[0]).keys())
        )
        writer.writeheader()
        for user in users:
            writer.writerow(user_to_dict(user))

    print(f"CSV sauvegardé : {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
