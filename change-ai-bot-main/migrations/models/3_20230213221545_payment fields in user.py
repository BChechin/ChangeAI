from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "payment_period" VARCHAR(5);
        ALTER TABLE "users" ADD "currency" VARCHAR(3);
        ALTER TABLE "users" ADD "payment_plan" VARCHAR(5);
        ALTER TABLE "users" ADD "payment_amount" INT;
        ALTER TABLE "users" ADD "last_payment_date" TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "payment_period";
        ALTER TABLE "users" DROP COLUMN "currency";
        ALTER TABLE "users" DROP COLUMN "payment_plan";
        ALTER TABLE "users" DROP COLUMN "payment_amount";
        ALTER TABLE "users" DROP COLUMN "last_payment_date";"""
