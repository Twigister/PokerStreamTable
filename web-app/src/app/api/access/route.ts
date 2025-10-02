import { NextRequest, NextResponse } from "next/server"

let counter = 0;

export async function GET(req: NextRequest) {
  ++counter;
  return NextResponse.json({ success: true, counter: counter})
}
